import json
import os

from config import MEMORY_FILE


def ensure_memory_file():

    folder = os.path.dirname(MEMORY_FILE)

    if not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists(MEMORY_FILE):

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                {
                    "memories": []
                },
                file,
                indent=4
            )


def load_memory():

    ensure_memory_file()

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {
            "memories": []
        }


def save_memory(data):

    ensure_memory_file()

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def remember(text):

    data = load_memory()

    memories = data.get(
        "memories",
        []
    )

    if text not in memories:

        memories.append(text)

    data["memories"] = memories

    save_memory(data)

    return "I will remember that."


def get_memories():

    data = load_memory()

    return data.get(
        "memories",
        []
    )


def clear_memory():

    save_memory(
        {
            "memories": []
        }
    )

    return "My memory has been cleared."