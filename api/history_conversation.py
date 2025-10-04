import os
from dotenv import load_dotenv


class HistoryConversation:
    def __init__(self):
        load_dotenv()
        self.__history = []

    def append_human_conversation(self, content: str):
        self.__history.append(f'Humano: {content}')

    def append_bot_conversation(self, content: str):
        self.__history.append(f'{os.getenv('PERSONA_NAME')}: {content}')

    def get_history(self) -> str:
        return '\n'.join(self.__history.copy())