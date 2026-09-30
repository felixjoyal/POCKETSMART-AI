import json

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..models import RecommendationHistory, User


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request,
            "error": request.query_params.get("error"),
        },
    )


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "request": request,
            "error": request.query_params.get("error"),
        },
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recent = db.scalars(
        select(RecommendationHistory)
        .where(RecommendationHistory.user_id == current_user.id)
        .order_by(RecommendationHistory.created_at.desc())
        .limit(5)
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "user": current_user,
            "recent": recent,
        },
    )


@router.get("/home-planner", response_class=HTMLResponse)
def home_planner(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        request=request,
        name="home_planner.html",
        context={
            "request": request,
            "user": current_user,
        },
    )


@router.get("/party-planner", response_class=HTMLResponse)
def party_planner(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        request=request,
        name="party_planner.html",
        context={
            "request": request,
            "user": current_user,
        },
    )


@router.get("/jewelry-planner", response_class=HTMLResponse)
def jewelry_planner(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        request=request,
        name="jewelry_planner.html",
        context={
            "request": request,
            "user": current_user,
        },
    )


@router.get("/history", response_class=HTMLResponse)
def history(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = db.scalars(
        select(RecommendationHistory)
        .where(RecommendationHistory.user_id == current_user.id)
        .order_by(RecommendationHistory.created_at.desc())
    ).all()

    items = [
        {
            "id": row.id,
            "planner_type": row.planner_type,
            "budget": row.budget,
            "created_at": row.created_at,
            "result": json.loads(row.result_json),
        }
        for row in rows
    ]

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "request": request,
            "user": current_user,
            "items": items,
        },
    )