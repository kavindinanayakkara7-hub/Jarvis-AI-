import os
from dotenv import load_dotenv

load_dotenv()

JARVIS_NAME = "JARVIS"

LANGUAGE = "en-US"

VOICE_RATE = 175
VOICE_VOLUME = 1.0

# AI
AI_ENABLED = os.getenv("AI_ENABLED", "true").lower() == "true"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

AI_MODEL = os.getenv(
    "AI_MODEL",
    "gpt-5-mini"
)

# Project paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MEMORY_FILE = os.path.join(
    BASE_DIR,
    "ai",
    "memory.json"
)

SCREENSHOT_DIR = os.path.join(
    BASE_DIR,
    "screenshots"
)

# Security
ALLOW_SYSTEM_SHUTDOWN = False
ALLOW_RESTART = False
ALLOW_SHELL_COMMANDS = False