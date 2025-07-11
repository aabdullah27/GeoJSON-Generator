from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import Optional, List, Dict, Any

# from ..schemas.json_schema import GeoJSONResponse
from ....services.doc_processor import document_processor_instance

router = APIRouter()

def get_document_processor():
    return document_processor_instance

# @router.post("/generate-geojson", response_model=GeoJSONResponse)
@router.post("/generate-geojson")
async def generate_geojson(
    file: UploadFile = File(...),
    document_category: str = Form(...)
):
    if document_category in ["csv", "xlsx"]:
        pass 
    elif document_category == "kml":
        pass
    else:
        raise HTTPException(status_code=400, detail="Invalid document category")

    return await get_document_processor().process_doc(file, document_category)
