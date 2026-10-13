import pyautogui
import time


def type_text(text):

    try:

        pyautogui.write(
            text,
            interval=0.02
        )

        return "Text typed successfully."

    except Exception as error:

        return f"Could not type text: {error}"


def press_key(key):

    try:

        pyautogui.press(
            key
        )

        return f"Pressed {key}."

    except Exception as error:

        return f"Could not press key: {error}"


def hotkey(*keys):

    try:

        pyautogui.hotkey(
            *keys
        )

        return "Keyboard shortcut executed."

    except Exception as error:

        return f"Keyboard shortcut failed: {error}"


def click(x, y):

    try:

        pyautogui.click(
            x,
            y
        )

        return f"Clicked at {x}, {y}."

    except Exception as error:

        return f"Mouse click failed: {error}"