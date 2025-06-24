import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

# --- Core Configuration ---
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-pro")

# --- Agent Specific Configuration ---
AGENT_NAME = 'book_writing_assistant'
AGENT_SYSTEM_INSTRUCTION = """You are a book writing assistant. Your task is to help users create books by following this process:

1. First, call the 'generate_book_outline' tool to create a structured outline based on the user's genre and preferences.
2. After generating the outline, call the 'write_chapter' tool to write individual chapters.
3. You can write multiple chapters in sequence by calling the 'write_chapter' tool repeatedly.

Always maintain consistency between chapters and follow the outline structure. When writing chapters, incorporate character development, engaging dialogue, and vivid descriptions appropriate to the genre."""

def get_config():
    """Returns a dictionary of key configurations."""
    config = {
        "GOOGLE_CLOUD_PROJECT": GOOGLE_CLOUD_PROJECT,
        "GOOGLE_CLOUD_LOCATION": GOOGLE_CLOUD_LOCATION,
        "GEMINI_MODEL_NAME": GEMINI_MODEL_NAME,
        "AGENT_NAME": AGENT_NAME,
        "AGENT_SYSTEM_INSTRUCTION": AGENT_SYSTEM_INSTRUCTION
    }
    # Basic validation
    if not GOOGLE_CLOUD_PROJECT:
        logger.warning("GOOGLE_CLOUD_PROJECT environment variable is not set. This is required for Vertex AI.")
    return config

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    conf = get_config()
    logger.info(f"Loaded configuration: {conf}")
    if not conf["GOOGLE_CLOUD_PROJECT"]:
        logger.error("Critical: GOOGLE_CLOUD_PROJECT must be set in your .env file for Vertex AI operations.")