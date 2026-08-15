import time

from google import genai
from google.genai import types
from django.conf import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def get_ai_response(conversation):

    messages = conversation.messages.order_by("created_at")

    history = []

    for message in messages:

        if message.role == "user":
            history.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part(text=message.content)
                    ]
                )
            )

        elif message.role == "assistant":
            history.append(
                types.Content(
                    role="model",
                    parts=[
                        types.Part(text=message.content)
                    ]
                )
            )

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=history
            )

            return response.text

        except Exception as e:

            print("GEMINI ERROR:", repr(e))
            raise