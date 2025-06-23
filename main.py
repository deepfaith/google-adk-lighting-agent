import asyncio
import logging
import sys
import os

# Add the project root to the Python path to ensure imports work correctly
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from lighting_agent.agent import LightingRecommendationAgent

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    setup_logging()
    try:
        agent = LightingRecommendationAgent()
        print("Welcome to the Lighting Recommendation Assistant! Type 'exit' to quit.")
        while True:
            user_query = input("\nPlease enter your lighting needs: ")
            if user_query.strip().lower() in ("exit", "quit"): 
                print("Goodbye!")
                break
            response = await agent.process_query(user_query)
            print("\n--- Assistant's Response ---")
            print(response)
            print("---------------------------")
    except Exception as e:
        logging.error(f"Error in main: {e}", exc_info=True)
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())