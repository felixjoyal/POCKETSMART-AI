from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import init_db
from .routers import api, auth, pages

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app=FastAPI(title=settings.app_name,description="AI-powered budget planning and recommendation assistant.",version="1.0.0",lifespan=lifespan)
app.mount("/static",StaticFiles(directory="static"),name="static")
app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(api.router)

@app.get("/health")
def health():
    return {"status":"ok","app":settings.app_name,"demo_mode":settings.demo_mode,"gemini_model":settings.gemini_model}
