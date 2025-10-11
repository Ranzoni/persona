from typing import Any

from history_conversation import ConversationType
from api_models import BaseResponse
from persona import Persona


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

def persona_to_response(persona: Persona) -> BaseResponse:
    persona_dict = {
        'id': persona.id(),
        'name': persona.name(),
        'prompt': persona.prompt()
    }

    return __any_to_response(
        success=True,
        source=persona_dict
    )