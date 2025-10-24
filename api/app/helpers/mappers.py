import uuid

from typing import Any

from app.infra.history_conversation import ConversationType
from app.models.api_models import BaseResponse
from app.models.persona import Persona
from app.helpers.security import IdGenerated


def __any_to_response(success: bool, source: Any) -> BaseResponse:
    response = BaseResponse(
        success=success,
        source=source
    )
    return response

def fail_response(source: str) -> BaseResponse:
    return __any_to_response(
        success=False,
        source=source
    )

def messages_history_to_response(messages_history: list[ConversationType]) -> BaseResponse:
    messages_dict = [
        {
            'who': msg.get_who(),
            'content': msg.get_content()
        }
        for msg in messages_history
    ]

    return __any_to_response(
        success=True,
        source=messages_dict
    )

def persona_message_to_response(message: str) -> BaseResponse:
    return __any_to_response(
        success=True,
        source=message
    )

def personas_list_to_response(personas: list[Persona]) -> BaseResponse:
    personas_dict = [
            {
                'id': persona.id(),
                'name': persona.name()
            }
            for persona in personas
        ]
    
    return __any_to_response(
        success=True,
        source=personas_dict
    )

def persona_to_response(persona: Persona, image_path: str) -> BaseResponse:
    persona_dict = {
        'id': persona.id(),
        'name': persona.name(),
        'fileName': persona.image(),
        'image': f'{image_path}/{persona.image()}'
    }

    return __any_to_response(
        success=True,
        source=persona_dict
    )

def id_generated_to_response(id_generated: IdGenerated) -> BaseResponse:
    id_generated_dict = {
        'id': id_generated.id(),
        'expiresIn': id_generated.expires_in(),
    }

    return __any_to_response(
        success=True,
        source=id_generated_dict
    )

def session_id_to_id_generated(session_id: str, expires_in: int) -> IdGenerated:
    try:
        uuid_str = session_id
        session_uuid = uuid.UUID(uuid_str)
        expires_timestamp = expires_in
        
        return IdGenerated(session_uuid, expires_timestamp)
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Invalid session ID: {e}")
