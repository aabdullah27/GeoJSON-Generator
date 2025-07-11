import pathlib
import tempfile
from fastapi import UploadFile
from google import genai

class DocProcessor:
    def __init__(self):
        self.client = genai.Client()
        self.model_name = "gemini-2.5-flash"

    async def process_doc(self, file: UploadFile, document_category: str):
        """Save Uploadfile to a temp path and uploads to Gemini File API."""

        suffix = pathlib.Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmpf:
            tmpf.write(await file.read())
            tmpf_path = tmpf.name

        try:
            print(f"Uploading {tmpf_path} to Gemini File API...")
            gemini_file = self.client.files.upload(file=tmpf_path)
            print(f"Upload Successful! For file: {tmpf_path}.")

            prompt = f"Process the following document of {document_category} and return the geojson of the document."
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=[prompt, gemini_file],
                config={"response_mime_type": "application/json"}
            )
            return response.text
        finally:
            pathlib.Path(tmpf_path).unlink(missing_ok=True)

document_processor_instance = Docrocessor()