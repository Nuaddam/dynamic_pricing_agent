from typing import List, Optional

from google import genai
from google.genai import types


def generate_content(
    parts: List[types.Part], system_instruction: Optional[str] = None, response_schema: Optional[types.SchemaUnion] = None
) -> types.GenerateContentResponse:
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=types.Content(
            parts=parts,
            role="user",
        ),
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_schema=response_schema,
            response_mime_type="application/json" if response_schema else None,
        ),
    )
    return response
