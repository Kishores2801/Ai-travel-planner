# Importing Packages
from google import genai
from src.config import Config
from google.genai import types

class GeminiClient:
    # Initialize the Gemini client with API Key and model configuration
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in the environment variables")
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model = Config.GEMINI_MODEL

    
    # Generating Text
    def generate_text(self, prompt: str, max_output_tokens=1024, temperature=0.2) -> str:
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        # This will be generate text
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,

                config= types.GenerateContentConfig(
                    temperature=temperature,
                max_output_tokens=max_output_tokens
                    ),
                
                
                )
            return response
        except Exception as e:
            raise RuntimeError(f'Error generating text: {str(e)}')

