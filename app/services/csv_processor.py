import pandas as pd
from fastapi import UploadFile
from .base_processor import BaseProcessor
import io

class CSVProcessor(BaseProcessor):
    async def process(self, file: UploadFile) -> str:
        try:
            content = await file.read()
            df = pd.read_csv(io.BytesIO(content))
            return df.to_string()
        except Exception as e:
            # Handle exceptions related to file reading or processing
            print(f"Error processing CSV file: {e}")
            raise
