import json

from repository import Repository


class ConversationType:
    def __init__(self, who: str, content: str):
        self.__who = who
        self.__content = content

    def get_who(self) -> str:
        return self.__who
    
    def get_content(self) -> str:
        return self.__content
    
class HistoryConversation:
    def __init__(self, id: str, persona_id: int):
        self.__id = f'{persona_id}__{id}'
        self.__is_connected = False
        self.__repo = Repository()
        self.__human = 'me'
        self.__bot = 'bot'

    def __connect(self):
        if self.__is_connected:
            return

        self.__repo.connect()
        self.__is_connected = True

    def __get_conversation_as_json(self, conversation_type: ConversationType) -> str:
        value_dict = {
            'who': conversation_type.get_who(),
            'content': conversation_type.get_content()
        }

        return json.dumps(value_dict, ensure_ascii=False)
    
    def __get_json_as_conversation(self, value: str) -> ConversationType:
        json_as_dict = json.loads(value)
        return ConversationType(
            who=json_as_dict['who'],
            content=json_as_dict['content']
        )

    def __append_conversation(self, who: str, content: str):
        conversation_type = ConversationType(who=who, content=content)

        self.__connect()
        self.__repo.insert_list(
            key=self.__id,
            value=self.__get_conversation_as_json(conversation_type)
        )

    def append_human_conversation(self, content: str):
        self.__append_conversation(self.__human, content)

    def append_bot_conversation(self, content: str):
        self.__append_conversation(self.__bot, content)

    def get_history(self, limit: int = None) -> list[ConversationType]:
        self.__connect()
        json_values = self.__repo.get_list(
            key=self.__id,
            limit=limit
        )

        return [self.__get_json_as_conversation(json) for json in json_values]
    
    def clear_history(self):
        self.__connect()
        self.__repo.remove(self.__id,)
