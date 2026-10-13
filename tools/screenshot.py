import os
import datetime
import pyautogui

from config import SCREENSHOT_DIR


def take_screenshot():

    try:

        os.makedirs(
            SCREENSHOT_DIR,
            exist_ok=True
        )

        filename = datetime.datetime.now().strftime(
            "screenshot_%Y%m%d_%H%M%S.png"
        )

        path = os.path.join(
            SCREENSHOT_DIR,
            filename
        )

        image = pyautogui.screenshot()

        image.save(path)

        return f"Screenshot saved to {path}."

    except Exception as error:

        return f"Screenshot failed: {error}"