An local AI chatbot who plays any charactere.

# How to run

## Configure the environment variables

- TEMPERATURE=The temperature value to the LLM process the response.
- CHAT_PROMPT=Persona prompt that you want to AI plays.
- PERSONA_NAME=The character name.

## Create the local environment

- Run: python -m venv venv
- Run: .\venv\Scripts\activate

### OBS: This is necessary to run the AI.

## Install dependencies

Run: pip install fastapi uvicorn python-dotenv langchain-ollama

## Run the AI

- Go to "main" folder
- Run: python main.py