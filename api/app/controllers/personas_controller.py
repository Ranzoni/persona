import os
import shutil
from fastapi import APIRouter, File, Request, Response, UploadFile

from app.controllers.base_controller import get_personas_data, handle_bad_request, handle_unauthorized
from app.helpers.mappers import fail_response, persona_to_response, personas_list_to_response
from app.helpers.security import api_secret_validator
from app.models.api_models import BaseResponse, PersonaRequest
from app.services.image import get_upload_dir


__personas_data = get_personas_data()

router = APIRouter()

@router.get('/')
def get_personas(response: Response):
    try:
        personas = __personas_data.get_all()
        return personas_list_to_response(personas)
    except Exception as e:
        return handle_bad_request(
            response=response,
            message=f'Fail to get the personas: {e}'
        )
    
@router.get('/{id}')
def get_persona_by_id(id: int, response: Response, request: Request):
    try:
        persona = __personas_data.get_by_id(id)
        return persona_to_response(
            persona,
            image_path=str(request.base_url) + 'images'
        )
    except Exception as e:
        return handle_bad_request(
            response=response,
            message=f'Fail to get the personas: {e}'
        )

@router.get('/{id}/prompt')
@api_secret_validator
def get_persona_prompt(id: int, response: Response, _: Request):
    try:
        persona = __personas_data.get_by_id(id)

        return BaseResponse(
            success=True,
            source=persona.prompt()
        )
    except Exception as e:
        return handle_bad_request(
            response=response,
            message=f'Fail to get the personas: {e}'
        )

@router.post('/')
@api_secret_validator
def create_persona(persona_request: PersonaRequest, _: Request, response: Response) -> BaseResponse:
    try:
        persona_created = __personas_data.include_persona(
            name=persona_request.name,
            prompt=persona_request.prompt
        )

        return persona_to_response(
            persona_created,
            image_path=get_upload_dir()
        )
    except Exception as e:
        return handle_bad_request(
            response=response,
            message=f'Fail to create a new persona: {e}'
        )
    
@router.put('/{id}')
@api_secret_validator
def update_persona(id: int, persona_request: PersonaRequest, _: Request, response: Response) -> BaseResponse:
    try:
        persona_updated = __personas_data.update_persona(
            id=id,
            name=persona_request.name,
            prompt=persona_request.prompt
        )
        if not persona_updated:
            return fail_response('Persona not found.')

        return persona_to_response(
            persona_updated,
            image_path=get_upload_dir()
        )
    except Exception as e:
        return handle_bad_request(
            response=response,
            message=f'Fail to update the persona: {e}'
        )

@router.delete('/{id}')
@api_secret_validator
def remove_persona(id: int, _: Request, response: Response) -> BaseResponse:
    try:
        persona_removed = __personas_data.remove_persona(id)
        if not persona_removed:
            return fail_response('Persona not found.')

        return BaseResponse(
            success=True,
            source='The persona was removed!'
        )
    except Exception as e:
        return handle_bad_request(
            response=response,
            message=f'Fail to remove the persona: {e}'
        )

@router.post("/{id}/upload")
@api_secret_validator
async def upload_image(id: int, _: Request, response: Response, file: UploadFile = File(...)):
    try:
        file_path = os.path.join(get_upload_dir(), file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        persona = __personas_data.get_by_id(id)
        if not persona:
            raise Exception('Persona not found.')
        
        __personas_data.update_persona(
            id=id,
            name=persona.name(),
            prompt=persona.prompt(),
            image=file.filename
        )

        return BaseResponse(
            success=True,
            source='The persona image was uploaded.'
        )
    except Exception as e:
        return handle_bad_request(
            response=response,
            message=f'Fail to upload the persona image: {e}'
        )