import json

from fastapi import UploadFile

from app.models.persona import Persona
from app.services.image import remove_image, save_image


class PersonaNotExistsError(Exception):
    '''
    Persona not exists exception raised for persona id not found.
    '''

    def __init__(self):
        self.__message = f'That persona not exists.'
        super().__init__(self.__message)

class PersonaNameExistsError(Exception):
    '''
    Persona name exists exception raised for persona name already included.

    Attributes:
        name -- persona name founded
    '''
    def __init__(self, name: str):
        self.__message = f'There is already a persona named {name}.'
        super().__init__(self.__message) 

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

    def __validate_persona_id(self, id: int):
        if not self.get_by_id(id):
            raise PersonaNotExistsError()

    def __persona_name_already_exists(self, name: str, id: int = None) -> bool:
        data = self.__load_personas()

        for character in data['characters']:
            if str(character['name']).lower() == name.lower():
                if id and int(character['id']) == id:
                    continue

                return True

        return False

    def __validate_persona_name(self, name: str, id: int = None):
        if self.__persona_name_already_exists(name, id):
            raise PersonaNameExistsError(name)

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
        self.__validate_persona_name(name)

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
    
    def update_persona(self, id: int, name: str, prompt: str, image: UploadFile = None) -> Persona | None:
        self.__validate_persona_id(id)
        self.__validate_persona_name(name=name, id=id)

        with open(self.__file_name, 'r+', encoding='utf-8') as f:
            data = json.load(f)

            character_index = None
            for i, character in enumerate(data['characters']):
                if character['id'] == id:
                    character_index = i
                    break
            
            if character_index is None:
                return None
            
            if image:
                if character['image']:
                    remove_image(character['image'])

                save_image(image)
            
            data['characters'][character_index] = {
                'id': id,
                'name': name,
                'prompt': prompt,
                'image': image.filename if image and image.filename else character['image']
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
        self.__validate_persona_id(id)
        
        with open(self.__file_name, 'r+', encoding='utf-8') as f:
            data = json.load(f)

            character_index = None
            for i, character in enumerate(data['characters']):
                if character['id'] == id:
                    character_index = i
                    break
            
            if character_index is None:
                return False
            
            image_name = data['characters'][character_index]['image']
            remove_image(image_name)
            del data['characters'][character_index]
            
            f.seek(0)
            f.truncate()
            json.dump(data, f, ensure_ascii=False, indent=2)


        return True
    