from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import Optional, List, Dict, Any, Type

# from ..schemas.json_schema import GeoJSONResponse
from ....services.ai_service import gemini_service_instance
from ....services.base_processor import BaseProcessor
from ....services.csv_processor import CSVProcessor
from ....services.excel_processor import ExcelProcessor
from ....services.kml_processor import KMLProcessor
from ....services.shp_processor import SHPProcessor

router = APIRouter()

# Processor mapping
PROCESSOR_MAPPING: Dict[str, Type[BaseProcessor]] = {
    "csv": CSVProcessor,
    "xlsx": ExcelProcessor,
    "kml": KMLProcessor,
    "kmz": KMLProcessor,
    "shp": SHPProcessor,
}

def get_gemini_service():
    return gemini_service_instance

# @router.post("/generate-geojson", response_model=GeoJSONResponse)
@router.post("/generate-geojson")
async def generate_geojson(
    file: UploadFile = File(...),
    document_category: str = Form(...)
):
    processor_class = PROCESSOR_MAPPING.get(document_category.lower())
    if not processor_class:
        raise HTTPException(status_code=400, detail=f"Invalid document category: {document_category}")

    try:
        processor = processor_class()
        parsed_doc_text = await processor.process(file)
        
        gemini_service = get_gemini_service()
        geojson_response = await gemini_service.generate_content(
            parsed_doc_text=parsed_doc_text,
            document_category=document_category
        )
        return geojson_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
