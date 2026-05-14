from google.genai import Client
from typing import Tuple
from contracts.agents import AgentBaseModel

_client = None

def get_client() -> Client:
    global _client
    
    if _client is None:
        _client = Client(api_key="api_key") # idont have apikey :( place your apikey here
        
    return _client

class Gemini(AgentBaseModel):
    __identify__ = "ea47c918-f156-4ec6-a515-80d247c96c4f"

    def __init__(self) -> None:
        super().__init__()
    
        self._model: str = "imagen-4.0-fast-generate-001" # gemini flash
        self._client = get_client()
        
    def _extract_parts(self, parts) -> Tuple[bool, str]:
        """
        
        """
        for part in parts:
            if getattr(part, "inline_data", None):
                img_data = part.inline_data.data
                status, path = self._image.save(
                    data={"agent": "Gemini", "parts": img_data}
                )
                
                if status:
                    return status, path
                
                return status, "Failed to save the File"

    def agent(self, prompt: str) -> Tuple[bool, str]:
        """
        
        """
        from google.genai.errors import ClientError
        from google.genai import types
        
        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=prompt,
                config=types.GenerateContentConfig(response_modalities=["IMAGE"])
            )

            parts = response.candidates[0].content.parts        
            status, reason = self._extract_parts(parts=parts)
        
            return status, reason
        except (ClientError, KeyError) as e:
            return False, e