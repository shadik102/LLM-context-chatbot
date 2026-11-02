
import os
import uuid
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )

MODEL = "gemini-3.5-flash-lite"
MAX_HISTORY_MESSAGES = 10

SYSTEM_PROMPT = """
You are a friendly and helpful AI assistant.
Answer accurately in simple language.
Keep answers clear and concise.
Remember information from earlier messages in the same conversation.
"""

client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(timeout=30000)
)

conversations = {}


def create_conversation():
    conversation_id = str(uuid.uuid4())
    conversations[conversation_id] = []
    return conversation_id


def send_message(conversation_id, user_message):
    if conversation_id not in conversations:
        raise ValueError("Conversation not found. Please start a new chat.")

    if not isinstance(user_message, str) or not user_message.strip():
        raise ValueError("Please enter a message.")

    message_text = user_message.strip()
    history = conversations[conversation_id]

    contents = []

    for item in history[-MAX_HISTORY_MESSAGES:]:
        contents.append({
            "role": item["role"],
            "parts": [{"text": item["text"]}]
        })

    contents.append({
        "role": "user",
        "parts": [{"text": message_text}]
    })

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.5,
                max_output_tokens=300
            )
        )

        answer = response.text

        if not answer or not answer.strip():
            raise RuntimeError("Gemini returned an empty response.")

        history.append({
            "role": "user",
            "text": message_text
        })

        history.append({
            "role": "model",
            "text": answer.strip()
        })

        return answer.strip()

    except Exception as error:
        print("GEMINI ERROR:", type(error).__name__, str(error))
        raise RuntimeError(
            f"{type(error).__name__}: {error}"
        ) from error


def get_conversation_history(conversation_id):
    if conversation_id not in conversations:
        raise ValueError("Conversation not found.")

    return conversations[conversation_id]
