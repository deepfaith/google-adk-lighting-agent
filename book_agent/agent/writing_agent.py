import asyncio
import logging
from pydantic import PrivateAttr
from google.adk.events.event import Event

from vertexai.generative_models import GenerativeModel, Part, Tool
from book_agent.config import get_config, AGENT_SYSTEM_INSTRUCTION 
from book_agent.tools.writing_tools import GENERATE_OUTLINE_VERTEX_TOOL, WRITE_CHAPTER_VERTEX_TOOL, AVAILABLE_WRITING_TOOLS

try:
    from google.adk.agents import BaseAgent
except ImportError:
    logging.warning("Could not import BaseAgent from google.adk. Using a placeholder.")
    class BaseAgent:
        pass 

logger = logging.getLogger(__name__)

class BookWritingAgent(BaseAgent):
    _config: dict = PrivateAttr()
    _model: GenerativeModel = PrivateAttr()
    _chat: object = PrivateAttr(default=None)

    def __init__(self, name="book_agent"):
        super().__init__(name=name)  
        self._config = get_config()
        if not self._config.get("GOOGLE_CLOUD_PROJECT") or not self._config.get("GOOGLE_CLOUD_LOCATION"):
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION must be set in environment."
            )
        
        self._model = GenerativeModel(
            self._config["GEMINI_MODEL_NAME"],
            system_instruction=[Part.from_text(AGENT_SYSTEM_INSTRUCTION)],
        )
        self._chat = None
        logger.info(f"BookWritingAgent initialized with model: {self._config['GEMINI_MODEL_NAME']}")

    async def start_session(self):
        """Starts a new chat session with the model."""
        self._chat = self._model.start_chat(
            history=[], 
            response_validation=False
        ) 
        logger.info("Chat session started with Vertex AI Gemini model.")

    async def process_query(self, user_query: str):
        if not self._chat:
            await self.start_session()

        logger.info(f"Sending user query to Vertex AI: '{user_query}'")
        
        try:
            # Initial query: Make the outline tool available first
            tools_for_this_call = [GENERATE_OUTLINE_VERTEX_TOOL]
            
            if not hasattr(self, '_chat') or self._chat is None:
                self._chat = self._model.start_chat(history=[], response_validation=False)
            
            response = await self._chat.send_message_async(user_query, tools=tools_for_this_call)
            
            # Process tool calls in a loop
            while (
                response.candidates
                and response.candidates[0].content.parts
                and getattr(response.candidates[0].content.parts[0], "function_call", None)
            ):
                function_call_part = response.candidates[0].content.parts[0]
                function_name = function_call_part.function_call.name
                
                if function_name in AVAILABLE_WRITING_TOOLS:
                    function_to_call = AVAILABLE_WRITING_TOOLS[function_name]
                    function_args = {key: value for key, value in function_call_part.function_call.args.items()}
                    
                    logger.info(f"Calling tool function: {function_name} with args: {function_args}")
                    tool_response_data = await function_to_call(**function_args)
                    logger.info(f"Tool function {function_name} response received")

                    response_content_part = Part.from_function_response(
                        name=function_name,
                        response=tool_response_data
                    )

                    # Determine tools for the next call based on the function just called
                    if function_name == "generate_book_outline":
                        # After outline generation, make chapter writing available
                        tools_for_this_call = [WRITE_CHAPTER_VERTEX_TOOL]
                        response = await self._chat.send_message_async(response_content_part, tools=tools_for_this_call)
                    elif function_name == "write_chapter":
                        # After chapter writing, continue with chapter writing tool
                        response = await self._chat.send_message_async(response_content_part, tools=[WRITE_CHAPTER_VERTEX_TOOL])
                    else:
                        logger.warn(f"Unexpected function {function_name} called in sequence.")
                        response = await self._chat.send_message_async(response_content_part)
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
                        outline = part.function_response.response.get("outline")
                        chapter_content = part.function_response.response.get("chapter_content")
                        summary = part.function_response.response.get("summary")
                        error = part.function_response.response.get("error")
                        
                        if error:
                            text_parts.append(f"Sorry, there was a problem: {error}")
                        elif outline:
                            text_parts.append("\n## Book Outline\n")
                            for idx, chapter in enumerate(outline, 1):
                                text_parts.append(f"Chapter {idx}: {chapter.get('title')}")
                                if chapter.get('sections'):
                                    for section in chapter.get('sections'):
                                        text_parts.append(f"  - {section}")
                            if summary:
                                text_parts.append(f"\nSummary: {summary}")
                        elif chapter_content:
                            text_parts.append(f"\n# {chapter_content.get('title', 'Chapter')}\n")
                            text_parts.append(chapter_content.get('content', ''))
                            
                if text_parts:
                    final_response_text = "\n\n".join(text_parts)
                    logger.info(f"Final response from Vertex AI generated")
                    return final_response_text
                else:
                    logger.error("No text part found in the final response from Vertex AI.")
                    return "Sorry, I couldn't generate a response for that query after processing."
        except Exception as e:
            logger.error(f"Error during Vertex AI interaction: {e}", exc_info=True)
            return f"An error occurred while processing your request: {e}"

    async def _run_async_impl(self, ctx):
        """Required by google-adk BaseAgent."""
        logger.info(f"ADK context object received")
        
        user_query = getattr(ctx, "user_input", None)
        if not user_query and hasattr(ctx, "input"):
            user_query = ctx.input
        if not user_query and hasattr(ctx, "query"):
            user_query = ctx.query
        if not user_query and hasattr(ctx, "user_content"):
            user_content = getattr(ctx, "user_content")
            if hasattr(user_content, "parts") and user_content.parts:
                texts = [getattr(part, "text", None) for part in user_content.parts if hasattr(part, "text") and part.text]
                if texts:
                    user_query = "\n".join(texts)
        if not user_query and hasattr(ctx, "__dict__"):
            for k, v in ctx.__dict__.items():
                if isinstance(v, str) and v.strip():
                    user_query = v
                    break
        if not user_query:
            yield Event(author=self.name, content={"parts": [{"text": "No user query found in context."}]}, partial=False)
            return

        response = await self.process_query(user_query)
        yield Event(author=self.name, content={"parts": [{"text": response}]}, partial=False)

# For Google ADK: an instance of the agent that the ADK can discover.
try:
    root_agent = BookWritingAgent(name="book_agent")
except Exception as e:
    logger.error(f"Failed to instantiate root_agent: {e}", exc_info=True)
    root_agent = None