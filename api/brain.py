import os

from langchain_ollama import ChatOllama
from dotenv import load_dotenv


def talk(prompt: str, message: str, messages_history: str):
    load_dotenv()

    try:
        llm = ChatOllama(
            model = 'gemma3:4b',
            validate_model_on_init = True,
            temperature = os.getenv('TEMPERATURE'),
        )

        system_prompt = f'O histórico do que foi conversado até agora:{messages_history}\n\n'

        system_prompt += prompt

        messages = [
            ('system', system_prompt),
            ('human', message),
        ]

        for chunk in llm.stream(messages):
            yield chunk.content
    except Exception as e:
        print(f'Erro na resposta da IA: {e}')
        return 'Só um minuto... Não consigo te responder agora.'
    