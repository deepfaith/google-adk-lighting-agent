import asyncio
import logging
import json
from pydantic import PrivateAttr
from google.adk.events.event import Event

from vertexai.generative_models import GenerativeModel, Part, Tool
from lighting_agent.config import get_config, AGENT_SYSTEM_INSTRUCTION 
from lighting_agent.tools.search_products_tool import SEARCH_PRODUCTS_VERTEX_TOOL, PRODUCT_DETAILS_VERTEX_TOOL, AVAILABLE_LIGHTING_TOOLS

try:
    from google.adk.agents import BaseAgent
except ImportError:
    logging.warning("Could not import BaseAgent from google.adk. Using a placeholder. Ensure google-adk is installed and provides BaseAgent.")
    class BaseAgent:
        pass 

logger = logging.getLogger(__name__)

class LightingRecommendationAgent(BaseAgent):
    _config: dict = PrivateAttr()
    _model: GenerativeModel = PrivateAttr()
    _chat: object = PrivateAttr(default=None)

    def __init__(self, name="lighting_agent"):
        super().__init__(name=name)  
        self._config = get_config()
        if not self._config.get("GOOGLE_CLOUD_PROJECT") or not self._config.get("GOOGLE_CLOUD_LOCATION"):
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION must be set in environment or .env file for Vertex AI."
            )
        
        self._model = GenerativeModel(
            self._config["GEMINI_MODEL_NAME"],
            system_instruction=[Part.from_text(AGENT_SYSTEM_INSTRUCTION)],
        )
        self._chat = None # Initialize chat session later
        logger.info(f"LightingRecommendationAgent initialized with model: {self._config['GEMINI_MODEL_NAME']}")

    async def start_session(self):
        """Starts a new chat session with the model."""
        self._chat = self._model.start_chat(
            history=[], 
            response_validation=False  # Disable response validation to avoid the error
        ) 
        logger.info("Chat session started with Vertex AI Gemini model.")

    async def process_query(self, user_query: str):
        if not self._chat:
            await self.start_session()

        logger.info(f"Sending user query to Vertex AI: '{user_query}'")
        
        try:
            # Initial query: Make the first tool (search_lighting_products) available
            tools_for_this_call = [SEARCH_PRODUCTS_VERTEX_TOOL]
            
            # Disable response validation to avoid the error
            if not hasattr(self, '_chat') or self._chat is None:
                self._chat = self._model.start_chat(history=[], response_validation=False)
            
            response = await self._chat.send_message_async(user_query, tools=tools_for_this_call)
            
            while (
                response.candidates
                and response.candidates[0].content.parts
                and getattr(response.candidates[0].content.parts[0], "function_call", None)
            ):
                function_call_part = response.candidates[0].content.parts[0]
                function_name = function_call_part.function_call.name
                
                if function_name in AVAILABLE_LIGHTING_TOOLS:
                    function_to_call = AVAILABLE_LIGHTING_TOOLS[function_name]
                    function_args = {key: value for key, value in function_call_part.function_call.args.items()}
                    
                    logger.info(f"Calling tool function: {function_name} with args: {function_args}")
                    tool_response_data = await function_to_call(**function_args)
                    logger.info(f"Tool function {function_name} response: {tool_response_data}")

                    response_content_part = Part.from_function_response(
                        name=function_name,
                        response=tool_response_data
                    )

                    # Determine tools for the *next* call based on the function just called
                    if function_name == "search_lighting_products":
                        # After search_lighting_products, make get_product_details available
                        tools_for_this_call = [PRODUCT_DETAILS_VERTEX_TOOL]
                        response = await self._chat.send_message_async(response_content_part, tools=tools_for_this_call)
                    elif function_name == "get_product_details":
                        # After get_product_details, no more tools expected in this sequence
                        response = await self._chat.send_message_async(response_content_part) # No 'tools' arg
                    else:
                        # Should not be reached if system prompt is followed for known tools
                        logger.warn(f"Unexpected function {function_name} called in sequence.")
                        response = await self._chat.send_message_async(response_content_part) # No 'tools' arg
                else:
                    logger.error(f"Unknown function call requested by model: {function_name}")
                    response_content_part = Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function {function_name}"} 
                    )
                    response = await self._chat.send_message_async(response_content_part)
                    break
            
            # Extract and return the final text response
            if response.candidates and response.candidates[0].content.parts:
                text_parts = []
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "text") and part.text:
                        text_parts.append(part.text)
                    if hasattr(part, "function_response") and part.function_response and isinstance(part.function_response.response, dict):
                        products = part.function_response.response.get("products")
                        product_details = part.function_response.response.get("product_details")
                        summary = part.function_response.response.get("summary")
                        error = part.function_response.response.get("error")
                        
                        if error:
                            text_parts.append(f"Sorry, there was a problem: {error}")
                        elif products:
                            text_parts.append("\nHere are the lighting products that match your criteria:")
                            for idx, p in enumerate(products, 1):
                                text_parts.append(
                                    f"{idx}. {p.get('name')} - ${p.get('price')}\n"
                                    f"   Type: {p.get('type')}, Lumens: {p.get('lumens')}, Location: {p.get('location')}"
                                )
                            if summary:
                                text_parts.append(f"\nSummary: {summary}")
                        elif product_details:
                            for product_id, details in product_details.items():
                                text_parts.append(f"\nProduct Details for {product_id}:")
                                text_parts.append(f"Description: {details.get('description')}")
                                specs = details.get('specifications', {})
                                text_parts.append(f"Specifications: {', '.join([f'{k}: {v}' for k, v in specs.items()])}")
                                reviews = details.get('reviews', {})
                                text_parts.append(f"Reviews: {reviews.get('average', 'N/A')}/5 ({reviews.get('count', 0)} reviews)")
                        elif summary:
                            text_parts.append(f"{summary}")
                            
                if text_parts:
                    final_response_text = "\n\n".join(text_parts)
                    logger.info(f"Final response from Vertex AI: {final_response_text}")
                    return final_response_text
                else:
                    logger.error("No text part found in the final response from Vertex AI.")
                    return "Sorry, I couldn't generate a response for that query after processing."
        except Exception as e:
            logger.error(f"Error during Vertex AI interaction: {e}", exc_info=True)
            return f"An error occurred while processing your request: {e}"

    async def _run_async_impl(self, ctx):
        """
        Required by google-adk BaseAgent. Handles a single invocation context.
        Yields events as required by the ADK event protocol.
        """
        logger.info(f"ADK context object: {ctx}")
        if hasattr(ctx, "__dict__"):
            logger.info(f"ADK context __dict__: {ctx.__dict__}")
        else:
            logger.info(f"ADK context dir: {dir(ctx)}")

        user_query = getattr(ctx, "user_input", None)
        if not user_query and hasattr(ctx, "input"):
            user_query = ctx.input
        if not user_query and hasattr(ctx, "query"):
            user_query = ctx.query
        # Try extracting from user_content.parts[0].text (ADK web UI pattern)
        if not user_query and hasattr(ctx, "user_content"):
            user_content = getattr(ctx, "user_content")
            if hasattr(user_content, "parts") and user_content.parts:
                texts = [getattr(part, "text", None) for part in user_content.parts if hasattr(part, "text") and part.text]
                if texts:
                    user_query = "\n".join(texts)
                    logger.info(f"Extracted user query from ctx.user_content.parts: {user_query}")
        # Try extracting from __dict__ as a fallback
        if not user_query and hasattr(ctx, "__dict__"):
            for k, v in ctx.__dict__.items():
                if isinstance(v, str) and v.strip():
                    logger.info(f"Found possible user query in ctx.__dict__: {k} = {v}")
                    user_query = v
                    break
        if not user_query:
            yield Event(author=self.name, content={"parts": [{"text": "No user query found in context."}]}, partial=False)
            return

        response = await self.process_query(user_query)
        yield Event(author=self.name, content={"parts": [{"text": response}]}, partial=False)

# For Google ADK: an instance of the agent that the ADK can discover.
try:
    root_agent = LightingRecommendationAgent(name="lighting_agent")
except Exception as e:
    logger.error(f"Failed to instantiate root_agent in lighting_agent.agent: {e}", exc_info=True)
    root_agent = None
