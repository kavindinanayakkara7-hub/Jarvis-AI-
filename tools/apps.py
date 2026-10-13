import os
import subprocess


APP_PATHS = {

    "chrome": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ],

    "vscode": [
        r"C:\Users\user\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    ],

    "notepad": [
        "notepad.exe"
    ],

    "calculator": [
        "calc.exe"
    ],

    "explorer": [
        "explorer.exe"
    ]
}


def open_app(app_name):

    app_name = app_name.lower().strip()

    paths = APP_PATHS.get(
        app_name
    )

    if not paths:

        return f"I don't know where {app_name} is installed."

    for path in paths:

        try:

            if path.endswith(".exe") and (
                os.path.exists(path)
                or path in [
                    "notepad.exe",
                    "calc.exe",
                    "explorer.exe"
                ]
            ):

                subprocess.Popen(
                    path
                )

                return f"Opening {app_name}."

        except Exception:
            continue

    return f"I could not open {app_name}."


def close_app(app_name):

    process_names = {

        "chrome": "chrome.exe",

        "vscode": "Code.exe",

        "notepad": "notepad.exe",

        "calculator": "CalculatorApp.exe"

    }

    process = process_names.get(
        app_name.lower()
    )

    if not process:

        return f"I don't know how to close {app_name}."

    try:

        subprocess.run(
            [
                "taskkill",
                "/IM",
                process,
                "/F"
            ],
            capture_output=True
        )

        return f"Closed {app_name}."

    except Exception:

        return f"Could not close {app_name}."