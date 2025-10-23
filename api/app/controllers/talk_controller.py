import os

from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse

from app.controllers.base_controller import get_personas_data, handle_bad_request
from app.helpers.security import get_session_id, session_validator
from app.infra.brain import talk
from app.infra.history_conversation import HistoryConversation
from app.models.api_models import BaseResponse, TalkRequest


__limit_messages_to_persona = int(os.getenv('LIMIT_MESSAGES_TO_PERSONA'))

router = APIRouter()

@router.post('/{persona_id}')
@session_validator
def talk_with_persona(persona_id: int, talk_request: TalkRequest, _: Request, response: Response) -> BaseResponse:
    try:
        persona = get_personas_data().get_by_id(persona_id)

        history = HistoryConversation(get_session_id(), persona.id())
        messages_history = history.get_history(limit=__limit_messages_to_persona)

        history.append_human_conversation(talk_request.message)

        def get_ai_response():
            try:
                persona_message = ''
                for answer in talk(persona.prompt(), talk_request.message, messages_history):
                    persona_message += answer
                    yield answer

                history.append_bot_conversation(persona_message)
            except Exception as e:
                yield f"Error generating response: {str(e)}"

        return StreamingResponse(
            get_ai_response(),
            media_type='text/plain',
            status_code=200
        )
    except Exception as e:
        return handle_bad_request(
            response=response,
            message=f'Fail to talk with the persona: {e}'
        )