from google import genai

class GeminiService:
    def __init__(self):
        self.client = genai.Client()
        self.model_name = "gemini-2.5-flash"

    async def generate_content(self, parsed_doc_text: str, document_category: str):
        try:
            prompt = f"Process the following document of {document_category} and return the geojson of the document."
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=[prompt, parsed_doc_text],
                config={"response_mime_type": "application/json"}
            )
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return None

gemini_service_instance = GeminiService()