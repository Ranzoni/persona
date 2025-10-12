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
        self.__file_name = 'characters.json'
        self.__data = []
        self.__personas: list[Persona] = []
        self.__load_personas()
        
    def __load_personas(self):
        self.__personas = []
        with open(self.__file_name, 'r', encoding='utf-8') as f:
            self.__data = json.load(f)

        for character in self.__data['characters']:
            persona = Persona(character['id'], character['name'], character['prompt'])
            self.__personas.append(persona)

    def __next_id(self) -> int:
        return len(self.__personas) + 1

    def get_all(self) -> list[Persona]:
        self.__load_personas()
        return self.__personas
    
    def get_by_id(self, id: int) -> Persona:
        self.__load_personas()
        return next((persona for persona in self.__personas if persona.id() == id), None)
    
    def include_persona(self, name: str, prompt: str):
        new_persona_dict = {
            "id": self.__next_id(),
            "name": name,
            "prompt": prompt
        }

        with open(self.__file_name, 'r+', encoding='utf-8') as f:
            self.__data = json.load(f)

            self.__data['characters'].append(new_persona_dict)

            f.seek(0) 
            f.truncate() 
            json.dump(self.__data, f, ensure_ascii=False, indent=2)

        return Persona(
            id=new_persona_dict['id'],
            name=new_persona_dict['name'],
            prompt=new_persona_dict['prompt'])
    
    def update_persona(self, id: int, name: str, prompt: str):
        with open(self.__file_name, 'r+', encoding='utf-8') as f:
            self.__data = json.load(f)
            
            persona_index = None
            for i, character in enumerate(self.__data['characters']):
                if character['id'] == id:
                    persona_index = i
                    break
            
            if persona_index is None:
                return None
            
            self.__data['characters'][persona_index] = {
                "id": id,
                "name": name,
                "prompt": prompt
            }
            
            f.seek(0)
            f.truncate()
            json.dump(self.__data, f, ensure_ascii=False, indent=2)
    
        return Persona(id=id, name=name, prompt=prompt)
    
    def remove_persona(self, id: int) -> bool:
        with open(self.__file_name, 'r+', encoding='utf-8') as f:
            self.__data = json.load(f)
            
            persona_index = None
            for i, character in enumerate(self.__data['characters']):
                if character['id'] == id:
                    persona_index = i
                    break
            
            if persona_index is None:
                return False
            
            del self.__data['characters'][persona_index]
            
            f.seek(0)
            f.truncate()
            json.dump(self.__data, f, ensure_ascii=False, indent=2)

        return True
    