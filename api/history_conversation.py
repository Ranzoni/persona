from repository import Repository


class HistoryConversation:
    def __init__(self, ip: str, persona_id: int):
        self.__id = f'{persona_id}__{ip}'
        self.__is_connected = False
        self.__repo = Repository()

    def __connect(self):
        if self.__is_connected:
            return

        self.__repo.connect()
        self.__is_connected = True

    def __append_conversation(self, who: str, content: str):
        self.__connect()
        self.__repo.insert(
            key=self.__id,
            value=f'{who}: {content}'
        )

    def append_human_conversation(self, content: str):
        self.__append_conversation('Humano', content)

    def append_bot_conversation(self, content: str):
        self.__append_conversation('Você', content)

    def get_history(self) -> list[str]:
        self.__connect()
        return self.__repo.get(key=self.__id)
    