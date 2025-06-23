import logging
from lighting_agent.agent import LightingRecommendationAgent, root_agent

logging.basicConfig(level=logging.INFO)
_agent_instance = None

def get_agent():
    """Provides a singleton instance of the LightingRecommendationAgent."""
    global _agent_instance
    if _agent_instance is None:
        try:
            # Use the existing root_agent if available
            if root_agent is not None:
                _agent_instance = root_agent
                logging.info("Using existing root_agent instance.")
            else:
                _agent_instance = LightingRecommendationAgent()
                logging.info("Created new LightingRecommendationAgent instance.")
        except Exception as e:
            logging.error(f"Failed to initialize LightingRecommendationAgent: {e}", exc_info=True)
            raise
    return _agent_instance

async def adk_request_handler(payload: dict):
    """
    A hypothetical request handler that an ADK web server might call.
    """
    agent = get_agent() # Ensure agent is initialized
    user_query = payload.get("query")

    if not user_query:
        logging.warning("ADK Handler: Missing 'query' in payload.")
        return {"error": "Missing 'query' in payload", "status_code": 400}

    logging.info(f"ADK Handler received query: '{user_query}'")
    try:
        response_text = await agent.process_query(user_query)
        logging.info(f"ADK Handler - Agent response: {response_text}")
        return {"response": response_text}
    except Exception as e:
        logging.error(f"Error processing query via ADK Handler: {e}", exc_info=True)
        return {"error": f"An internal error occurred: {str(e)}", "status_code": 500}
