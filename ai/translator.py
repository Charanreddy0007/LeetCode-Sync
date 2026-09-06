import os
import io
import config
import contextlib

from pathlib import Path
from google import genai
from google.genai import types, errors
from pydantic import BaseModel


class TranslationResult(BaseModel):
    python: str
    cpp: str
    javascript: str
    typescript: str
    java: str


def translate_solution(solution: str, source_language: str) -> dict:

    api_key = os.getenv("GEMINI_API_KEY")
    gemini_model = os.getenv("GEMINI_MODEL")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set."
        )

    # Find prompt.txt next to this file
    prompt_path = Path(__file__).parent / "prompt.txt"

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {prompt_path}"
        )

    prompt = prompt_path.read_text(encoding="utf-8")

    # Insert values into the prompt
    prompt = prompt.replace(
        "{{SOURCE_LANGUAGE}}",
        source_language
    )

    prompt = prompt.replace(
        "{{SOLUTION}}",
        solution
    )

    # Create Gemini client
    client = genai.Client(api_key=api_key)

    # Generate structured JSON
    try:
        with (
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            response = client.models.generate_content(
                model=gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=TranslationResult,
                ),
            )

        # Validate Gemini's JSON response
        result = TranslationResult.model_validate_json(response.text)
        print("    Ai response is Done ✓")
        return result.model_dump()
    
    except errors.APIError as e:

        print(e.code, str(e))
    
    except Exception as e:
        print(500, str(e))