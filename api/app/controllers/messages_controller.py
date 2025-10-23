import os

from fastapi import APIRouter, Request, Response

from app.controllers.base_controller import get_personas_data, handle_bad_request
from app.helpers.mappers import messages_history_to_response
from app.helpers.security import get_session_id, session_validator
from app.infra.history_conversation import HistoryConversation
from app.models.api_models import BaseResponse


__limit_messages_to_response = int(os.getenv('LIMIT_MESSAGES_TO_RESPONSE'))

router = APIRouter()

__personas_data = get_personas_data()

@router.get('/{persona_id}')
@session_validator
def get_messages(persona_id: int, _: Request, response: Response) -> BaseResponse:
    try:
        persona = __personas_data.get_by_id(persona_id)

        history = HistoryConversation(get_session_id(), persona.id())
        messages_history = history.get_history(limit=__limit_messages_to_response)

        return messages_history_to_response(messages_history)
    except Exception as e:
        return handle_bad_request(
            response=response,
            message=f'Fail to get the history messages: {e}'
        )

@router.delete('/{persona_id}')
@session_validator
def remove_messages(persona_id: int, _: Request, response: Response) -> BaseResponse:
    try:
        history = HistoryConversation(get_session_id(), persona_id)

        history.clear_history()

        return BaseResponse(
            success=True,
            source={'Messages cleared.'}
        )
    except Exception as e:
        return handle_bad_request(
            response=response,
            message=f'Fail to remove the messages: {e}'
        )
