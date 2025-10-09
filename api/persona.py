import json


class Persona:
    def __init__(self, id, name, prompt):
        self.__id = id
        self.__name = name
        self.__prompt = prompt

    def id(self) -> int:
        return self.__id
    
    def name(self) -> str:
        return self.__name
    
    def prompt(self) -> str:
        return self.__prompt

class PersonasData:
    def __init__(self):
        self.__data = []
        self.__personas: list[Persona] = []

        with open('characters.json', 'r', encoding='utf-8') as f:
            self.__data = json.load(f)
            
        self.__populate_personas()
        
    def __populate_personas(self):
        for character in self.__data['characters']:
            persona = Persona(character['id'], character['name'], character['prompt'])
            self.__personas.append(persona)

    def get_all(self) -> list[Persona]:
        return self.__personas
    
    def get_by_id(self, id: int) -> Persona:
        return next((persona for persona in self.__personas if persona.id() == id), None)