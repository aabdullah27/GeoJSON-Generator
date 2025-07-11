from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Loading Environment Variables
load_dotenv()

# Codebase Imports
from app.core.config import settings
from app.api.v1 import api_router_v1

# setup main app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}.openapi.json"
)

# setting up cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# setting up API router
app.include_router(api_router_v1, prefix=settings.API_V1_STR)

# Welcome Route
@app.get("/")
async def root():
    return {"message": "Welcome! To the GeoJSON Generator API"}
