import json

from app.models.persona import Persona


class PersonasData:
    def __init__(self):
        self.__file_name = 'characters.json'
        
    def __load_personas(self) -> list:
        data = []
        with open(self.__file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data

    def __next_id(self) -> int:
        data = self.__load_personas()
        return len(data['characters']) + 1

    def get_all(self) -> list[Persona]:
        data = self.__load_personas()

        personas: list[Persona] = []
        for character in data['characters']:
            persona = Persona(character['id'], character['name'], character['prompt'], character['image'])
            personas.append(persona)

        return sorted(personas, key=lambda persona: persona.name())
    
    def get_by_id(self, id: int) -> Persona | None:
        data = self.__load_personas()

        persona: Persona = None
        for character in data['characters']:
            if int(character['id']) == id:
                persona = Persona(character['id'], character['name'], character['prompt'], character['image'])
                break

        return persona
    
    def include_persona(self, name: str, prompt: str) -> Persona:
        new_persona_dict = {
            'id': self.__next_id(),
            'name': name,
            'prompt': prompt,
            'image': ''
        }

        with open(self.__file_name, 'r+', encoding='utf-8') as f:
            data = json.load(f)

            data['characters'].append(new_persona_dict)

            f.seek(0) 
            f.truncate() 
            json.dump(data, f, ensure_ascii=False, indent=2)

        return Persona(
            id=new_persona_dict['id'],
            name=new_persona_dict['name'],
            prompt=new_persona_dict['prompt']
        )
    
    def update_persona(self, id: int, name: str, prompt: str, image: str = None) -> Persona | None:
        with open(self.__file_name, 'r+', encoding='utf-8') as f:
            data = json.load(f)

            character_index = None
            for i, character in enumerate(data['characters']):
                if character['id'] == id:
                    character_index = i
                    break
            
            if character_index is None:
                return None
            
            data['characters'][character_index] = {
                'id': id,
                'name': name,
                'prompt': prompt,
                'image': image if image else character['image']
            }
            
            f.seek(0)
            f.truncate()
            json.dump(data, f, ensure_ascii=False, indent=2)
    
        return Persona(
            id=id,
            name=name,
            prompt=prompt
        )
    
    def remove_persona(self, id: int) -> bool:
        with open(self.__file_name, 'r+', encoding='utf-8') as f:
            data = json.load(f)

            character_index = None
            for i, character in enumerate(data['characters']):
                if character['id'] == id:
                    character_index = i
                    break
            
            if character_index is None:
                return False
            
            del data['characters'][character_index]
            
            f.seek(0)
            f.truncate()
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True
    