
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise SystemExit("Gemini API key missing. Check your .env file.")

try:
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=30000)
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Explain what an API is in two simple sentences.",
        config=types.GenerateContentConfig(
            max_output_tokens=100,
            temperature=0.5
        )
    )

    print("\n=== GEMINI API TEST ===")
    print(response.text)

except Exception as error:
    print("\nGemini API request failed.")
    print("Error type:", type(error).__name__)
    print("Error message:", str(error))

