class Persona:
    def __init__(self, id, name, prompt, image = None):
        self.__id = id
        self.__name = name
        self.__prompt = prompt
        self.__image = image

    def id(self) -> int:
        return self.__id
    
    def name(self) -> str:
        return self.__name
    
    def prompt(self) -> str:
        return self.__prompt
    
    def image(self) -> str | None:
        return self.__image

