import os
import sys
import json
from typing import Any, Dict, Type
from pydantic import BaseModel

try:
    from mistralai import Mistral
except ImportError:
    Mistral = None

class MistralLLM:
    def __init__(self, api_key: str = None, model: str = "mistral-large-latest"):
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        self.model = model
        
        self.client = None
        if Mistral and self.api_key:
            self.client = Mistral(api_key=self.api_key)

    def generate_structured(self, prompt: str, response_model: Type[BaseModel]) -> BaseModel:
        """
        Generates a structured response using Mistral JSON mode.
        """
        if not self.client:
             raise ValueError("Mistral Client not initialized. Please set MISTRAL_API_KEY env var and install `mistralai`.")

        system_prompt = f"""
        You are a helpful AI assistant.
        Output your response strictly in valid JSON format matching the following schema id:
        {json.dumps(response_model.model_json_schema(), indent=2)}
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        chat_response = self.client.chat.complete(
            model=self.model,
            messages=messages
        )

        import re
        response_content = chat_response.choices[0].message.content
        
        # Strip markdown code fencing if present
        if "```" in response_content:
            response_content = re.sub(r"```json\s*", "", response_content)
            response_content = re.sub(r"```\s*", "", response_content)
            response_content = response_content.strip()
        
        try:
            # Parse JSON and validate with Pydantic
            data = json.loads(response_content)
            return response_model.model_validate(data)
        except json.JSONDecodeError:
            with open("bad_json.txt", "w", encoding="utf-8") as f:
                f.write(response_content)
            print(f"DEBUG: Failed Raw Response: {response_content}", file=sys.stderr)
            raise ValueError(f"Failed to decode JSON from LLM response. Content saved to bad_json.txt")
        except Exception as e:
             with open("bad_json.txt", "w", encoding="utf-8") as f:
                f.write(response_content)
             print(f"DEBUG: Validation Error: {e}\nRaw: {response_content[:200]}...", file=sys.stderr)
             raise ValueError(f"Validation failed: {e}")

    def generate_text(self, prompt: str) -> str:
        if not self.client:
             raise ValueError("Mistral Client not initialized. Please set MISTRAL_API_KEY env var.")

        messages = [
            {"role": "user", "content": prompt}
        ]

        chat_response = self.client.chat.complete(
            model=self.model,
            messages=messages
        )

        return chat_response.choices[0].message.content
