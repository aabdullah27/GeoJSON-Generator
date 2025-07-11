from fastapi import APIRouter
from .endpoints import generator

api_router_v1 = APIRouter()
api_router_v1.include_router(generator.router, prefix="/generator", tags=["GeoJSON-Generator"])