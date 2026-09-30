from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from ..auth import COOKIE_NAME, authenticate_user, create_access_token, hash_password
from ..database import get_db
from ..models import User

router = APIRouter()

@router.post("/register")
def register(username: str=Form(...), email: str=Form(...), password: str=Form(...), db: Session=Depends(get_db)):
    username, email = username.strip(), email.strip().lower()
    if len(username) < 3 or len(password) < 8:
        return RedirectResponse("/register?error=Username+or+password+is+too+short", status_code=303)
    if db.scalar(select(User).where(or_(User.username==username, User.email==email))):
        return RedirectResponse("/register?error=Username+or+email+already+exists", status_code=303)
    db.add(User(username=username, email=email, password_hash=hash_password(password)))
    db.commit()
    return RedirectResponse("/login?registered=1", status_code=303)

@router.post("/login")
def login(username: str=Form(...), password: str=Form(...), db: Session=Depends(get_db)):
    user = authenticate_user(db, username.strip(), password)
    if not user:
        return RedirectResponse("/login?error=Invalid+username+or+password", status_code=303)
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie(COOKIE_NAME, create_access_token(user.id), httponly=True, secure=False, samesite="lax", max_age=86400)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(COOKIE_NAME)
    return response
