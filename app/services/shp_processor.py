from fastapi import UploadFile
from .base_processor import BaseProcessor
import geopandas as gpd
from zipfile import ZipFile
import io
import os
import tempfile

class SHPProcessor(BaseProcessor):
    async def process(self, file: UploadFile) -> str:
        try:
            content = await file.read()
            
            with tempfile.TemporaryDirectory() as temp_dir:
                if file.filename.lower().endswith('.zip'):
                    with ZipFile(io.BytesIO(content), 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                    
                    shp_files = [f for f in os.listdir(temp_dir) if f.lower().endswith('.shp')]
                    if not shp_files:
                        raise ValueError("No .shp file found in the zip archive.")
                    
                    shp_path = os.path.join(temp_dir, shp_files[0])
                    gdf = gpd.read_file(shp_path)
                    
                else:
                    raise ValueError("Shapefiles must be uploaded as a .zip archive.")

                return gdf.to_string()

        except Exception as e:
            print(f"Error processing SHP file: {e}")
            raise 