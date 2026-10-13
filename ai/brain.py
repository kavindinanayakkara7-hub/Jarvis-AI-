import json
import urllib.request
import urllib.error

from config import (
    AI_ENABLED,
    OPENAI_API_KEY,
    AI_MODEL
)

from ai.memory import get_memories
from ai.planner import create_plan


SYSTEM_PROMPT = """
You are JARVIS, a powerful desktop AI assistant.

You control a Windows computer through safe tools.

You must understand natural language.

Do NOT assume that the user must use predefined commands.

The user can describe tasks naturally.

Available actions:

open_app
open_website
search_web
create_folder
create_file
find_files
type_text
press_key
take_screenshot
get_system_info
get_current_time
remember
get_memory
clear_memory
set_volume
chat

Return ONLY valid JSON.

For a single action:

{
    "type": "action",
    "action": "open_app",
    "parameters": {
        "app": "chrome"
    }
}

For multiple actions:

{
    "type": "multi_action",
    "actions": [
        {
            "action": "open_app",
            "parameters": {
                "app": "chrome"
            }
        },
        {
            "action": "search_web",
            "parameters": {
                "query": "Python AI tutorials"
            }
        }
    ]
}

For normal conversation:

{
    "type": "chat",
    "message": "..."
}

For memory:

{
    "type": "action",
    "action": "remember",
    "parameters": {
        "text": "..."
    }
}

Be concise.

Never return markdown.

Never return explanations outside JSON.
"""


def build_prompt(user_text):

    memories = get_memories()

    memory_text = "\n".join(
        f"- {memory}"
        for memory in memories[-20:]
    )

    return f"""
USER MEMORY:
{memory_text}

USER REQUEST:
{user_text}
"""


def ask_ai(question):

    if not AI_ENABLED:

        return {
            "type": "chat",
            "message": "AI mode is currently disabled."
        }

    if not OPENAI_API_KEY:

        return {
            "type": "chat",
            "message": "AI API key is not configured yet."
        }

    prompt = build_prompt(question)

    payload = {
        "model": AI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    data = json.dumps(
        payload
    ).encode("utf-8")

    request = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=60
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        content = result["choices"][0]["message"]["content"]

        return create_plan(content)

    except urllib.error.HTTPError as error:

        try:
            error_body = error.read().decode()

            print(
                "AI HTTP Error:",
                error_body
            )

        except Exception:
            pass

        return {
            "type": "chat",
            "message": f"AI request failed: {error.code}"
        }

    except Exception as error:

        print(
            "AI Error:",
            error
        )

        return {
            "type": "chat",
            "message": "I could not connect to the AI service."
        }