import os
import json
import google.generativeai as genai
from typing import Dict, Any
from dotenv import load_dotenv

class GeminiClient:
    """
    Wrapper for Gemini API to handle structured generation 
    based on AgentSkill schemas.
    """
    def __init__(self, model_name: str = "gemini-1.5-pro"):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_structured(self, system_instruction: str, user_prompt: str) -> Dict[str, Any]:
        """
        Calls Gemini and forces a JSON response.
        """
        # Using Gemini's controlled output via response_mime_type
        generation_config = {
            "response_mime_type": "application/json",
        }
        
        full_prompt = f"{system_instruction}\n\nUser Input:\n{user_prompt}"
        
        response = self.model.generate_content(
            full_prompt, 
            generation_config=generation_config
        )
        
        return json.loads(response.text)