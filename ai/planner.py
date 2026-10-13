import json


def extract_json(text):

    if not text:
        return None

    text = text.strip()

    try:
        return json.loads(text)

    except Exception:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:

        try:

            return json.loads(
                text[start:end + 1]
            )

        except Exception:
            return None

    return None


def create_plan(ai_response):

    plan = extract_json(ai_response)

    if not plan:
        return {
            "type": "chat",
            "message": ai_response
        }

    return plan