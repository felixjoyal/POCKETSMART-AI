import json, os, uuid
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from ..config import settings
from ..database import get_db
from ..dependencies import get_current_user
from ..models import RecommendationHistory, User
from ..schemas import HomeRequest, JewelryRequest, PartyRequest, RecommendationResponse
from ..services.platform_links import add_links
from ..services.recommendation_service import generate_home, generate_jewelry, generate_party

router = APIRouter(prefix="/api")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_TYPES = {"image/jpeg","image/png","image/webp"}

def _save(db, user, planner_type, budget, input_data, result):
    result_dict = add_links(result.model_dump())
    db.add(RecommendationHistory(
        user_id=user.id, planner_type=planner_type, budget=budget,
        input_json=json.dumps(input_data, ensure_ascii=False),
        result_json=json.dumps(result_dict, ensure_ascii=False)
    ))
    db.commit()
    return RecommendationResponse.model_validate(result_dict)

@router.get("/me")
def me(current_user: User=Depends(get_current_user)):
    return {"id":current_user.id,"username":current_user.username,"email":current_user.email}

@router.post("/generate-home", response_model=RecommendationResponse)
def generate_home_api(data: HomeRequest, current_user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    try: return _save(db,current_user,"home",data.budget,data.model_dump(),generate_home(data))
    except Exception as exc: raise HTTPException(502, detail=str(exc)) from exc

@router.post("/generate-party", response_model=RecommendationResponse)
def generate_party_api(data: PartyRequest, current_user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    try: return _save(db,current_user,"party",data.budget,data.model_dump(),generate_party(data))
    except Exception as exc: raise HTTPException(502, detail=str(exc)) from exc

@router.post("/generate-jewelry", response_model=RecommendationResponse)
async def generate_jewelry_api(
    budget:int, occasion:str, style:str, preferences:str="",
    outfit_image:UploadFile|None=File(default=None),
    current_user:User=Depends(get_current_user), db:Session=Depends(get_db)
):
    image_path=None
    try:
        data=JewelryRequest(budget=budget,occasion=occasion,style=style,preferences=preferences)
        if outfit_image:
            if outfit_image.content_type not in ALLOWED_TYPES:
                raise HTTPException(400, detail="Only JPG, PNG, and WEBP images are supported.")
            raw=await outfit_image.read()
            if len(raw)>settings.max_upload_mb*1024*1024:
                raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=f"Image must be <= {settings.max_upload_mb} MB.")
            suffix={"image/jpeg":".jpg","image/png":".png","image/webp":".webp"}[outfit_image.content_type]
            image_path=str(UPLOAD_DIR/f"{uuid.uuid4().hex}{suffix}")
            Path(image_path).write_bytes(raw)
        return _save(db,current_user,"jewelry",data.budget,{**data.model_dump(),"outfit_image":bool(outfit_image)},generate_jewelry(data,image_path))
    except HTTPException: raise
    except Exception as exc: raise HTTPException(502, detail=str(exc)) from exc
    finally:
        if image_path and os.path.exists(image_path):
            try: os.remove(image_path)
            except OSError: pass



# Documentation-compatible endpoint aliases.
@router.post("/generate-home", response_model=RecommendationResponse)
def generate_home_root_alias(data: HomeRequest, current_user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    return generate_home_api(data, current_user, db)

@router.post("/generate-party", response_model=RecommendationResponse)
def generate_party_root_alias(data: PartyRequest, current_user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    return generate_party_api(data, current_user, db)

@router.get("/history")
def history_api(current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    rows=db.query(RecommendationHistory).filter(RecommendationHistory.user_id==current_user.id).order_by(RecommendationHistory.created_at.desc()).all()
    return [{"id":r.id,"planner_type":r.planner_type,"budget":r.budget,"created_at":r.created_at.isoformat(),"result":json.loads(r.result_json)} for r in rows]

@router.get("/recommendations/{recommendation_id}")
def recommendation_detail(recommendation_id:int,current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    row=db.get(RecommendationHistory,recommendation_id)
    if not row or row.user_id!=current_user.id: raise HTTPException(404,detail="Recommendation not found.")
    return json.loads(row.result_json)
