# 💡 Smart Lighting Recommendation Agent

Hey there! Welcome to the Lighting Recommendation Agent project. This is a smart AI assistant that helps you find the best lighting products by combining the power of Google's ADK (Agent Development Kit) with Vertex AI's Gemini model.

## What does it do?

This little genius will:
- Chat with you about your lighting needs through a friendly web interface
- Search for lighting products based on your requirements (type, location, price, etc.)
- Get detailed information about specific products that match your criteria
- Show you nicely formatted results with all the details you need

Think of it as having your own AI lighting consultant that's always ready to help!

## Cool features

- **Works with Google ADK**: Built on Google's Agent Development Kit for a smooth experience
- **Smart conversation**: Understands what you're asking even when queries come in different formats
- **Detailed product information**: Provides comprehensive details about lighting products
- **Developer-friendly**: Easy to extend with more tools or customize for your needs
- **Helpful logging**: Keeps track of what's happening to make debugging a breeze

## Getting started

### 1. Set up your environment

First, clone this repo to your local machine, then:

```sh
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the requirements
pip install -r requirements.txt
```

### 2. Set up your credentials

Create a `.env` file in the project root with these variables:

```
# Required settings
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1  # or your preferred region
GEMINI_MODEL_NAME=gemini-1.5-pro  # or your preferred Gemini model
```

You can copy these from the included `.env.example` file.

### 3. Run the agent

It's as simple as:

```sh
adk web
```

The ADK web interface will open, and you can start chatting with your lighting agent!

For local testing without the ADK web interface, you can also run:

```sh
python main.py
```

## Using your lighting agent

Just type queries like:
- "I need LED floodlights for my warehouse"
- "Find me energy-efficient lighting for my outdoor space under $200"
- "What are the best high bay lights with at least 15000 lumens?"

The agent will do the rest - searching for products and presenting you with the best options.

## Sample questions to try

Here are some specific questions you can try to test different features of the agent:

### Basic product search
- "I need LED lights for my garage"
- "Show me some floodlights"
- "What lighting options do you have for a warehouse?"

### Searching with specific criteria
- "Find me energy-efficient outdoor lights under $200"
- "I need high bay lights with at least 15000 lumens"
- "Show me LED floodlights for outdoor use that are energy efficient"
- "What lighting products do you have from LightMaster brand?"

### Searching with multiple criteria
- "I need energy-efficient LED lights for my warehouse that are at least 12000 lumens and under $200"
- "Find me outdoor lighting with 5000K color temperature from IndustrialLux"
- "What are the brightest warehouse lights you have that are energy efficient?"

### Getting detailed information
- "Tell me more about the OutdoorBright LED Floodlight"
- "What are the specifications for the Industrial LED High Bay?"
- "I want to know more about product LED-OUT-001"

The agent will first search for products matching your criteria, then automatically get detailed information about the best matches, and finally present you with comprehensive recommendations.

## Troubleshooting

Running into issues? Here are some common fixes:

- **Getting "No user query found"**: This usually means there's an issue with how the ADK is passing user input to the agent. Check the logs for details on the context object.

- **Seeing tool call errors**: Make sure both tools are provided in `send_message_async` calls - the model needs to know what tools are available.

- **Google Auth errors**: Make sure your Google Cloud credentials are properly set up:
  ```
  gcloud auth application-default login
  gcloud config set project your-project-id
  ```

- **Model not found errors**: Ensure you're using a valid Gemini model name that's available in your region. Try `gemini-1.5-pro` or `gemini-1.0-pro` if you encounter issues.

- **Issues with ADK web UI**: If the ADK web UI doesn't appear to be working correctly:
  - Make sure you have the latest version of the Google ADK
  - Try restarting the service with `adk web --restart`
  - Check the console for any error messages

## Project structure

- `lighting_agent/agent/recommendation_agent.py` - The brains of the operation
- `lighting_agent/tools/search_products_tool.py` - The product search tools
- `lighting_agent/config.py` - Configuration settings
- `requirements.txt` - All the Python packages you need

## Want to extend it?

This agent is designed to be modular - you can easily:
- Add more product search tools
- Change how results are displayed
- Modify the system prompt to handle different kinds of lighting queries

For local testing without the ADK web interface, check out the `main.py` script.

## License

MIT - Feel free to use this code however you'd like!