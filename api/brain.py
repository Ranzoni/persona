import os

from langchain_ollama import ChatOllama
from dotenv import load_dotenv

from history_conversation import ConversationType


def talk(prompt: str, message: str, messages_history: list[ConversationType]):
    load_dotenv()

    try:
        llm = ChatOllama(
            model = 'gemma3:4b',
            validate_model_on_init = True,
            temperature = os.getenv('TEMPERATURE'),
        )

        previous_messages = ''
        for message_history in messages_history:
            previous_messages += f'{message_history.get_who()}: {message_history.get_content()}\n'

        system_prompt = f'O histórico do que foi conversado até agora:{previous_messages}\n\n'

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
    