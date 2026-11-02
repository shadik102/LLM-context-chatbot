import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise SystemExit(
        "API key not found. Please check your .env file."
    )

client = OpenAI(api_key=api_key)

try:
    response = client.responses.create(
        model="gpt-5.5",
        instructions=(
            "You are a friendly Python programming tutor. "
            "Explain concepts simply and clearly."
        ),
        input="Explain what an API is in two simple sentences.",
        timeout=30.0,
    )

    print("\n=== LLM API TEST ===")
    print(response.output_text)

except Exception as error:
    print("\nAPI request failed.")
    print(f"Error type: {type(error).__name__}")
    print(f"Status code: {getattr(error, 'status_code', 'Unknown')}")
    print(f"Error code: {getattr(error, 'code', 'Unknown')}")
    print(f"Error message: {getattr(error, 'message', str(error))}")