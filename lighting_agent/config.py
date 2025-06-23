import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

# --- Core Configuration ---
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME") # Or your preferred model for Vertex AI

# --- Agent Specific Configuration ---
AGENT_NAME = 'lighting_recommendation_assistant'
AGENT_SYSTEM_INSTRUCTION = """Your SOLE first task is to call the 'search_lighting_products' tool. Do NOT ask questions. Do NOT respond with text. Extract parameters from the user's query and call 'search_lighting_products' IMMEDIATELY.
After 'search_lighting_products' is called, your SOLE second task is to call 'get_product_details'. Do NOT ask questions. Do NOT respond with text. Use product IDs from the search results and call 'get_product_details' IMMEDIATELY.
After BOTH tools are called, then and ONLY then, analyze their combined results and provide a text summary to the user with product recommendations."""

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
