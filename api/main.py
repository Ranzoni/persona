import uvicorn
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from brain import talk
from history_conversation import HistoryConversation
from mappers import fail_response, messages_history_to_response, persona_message_to_response, persona_to_response, personas_list_to_response
from persona import PersonasData
from api_models import BaseResponse, PersonaRequest, TalkRequest
from security import generate_random_id, validate_secret_key


load_dotenv()
__limit_messages_to_persona = int(os.getenv('LIMIT_MESSAGES_TO_PERSONA'))
__limit_messages_to_response = int(os.getenv('LIMIT_MESSAGES_TO_RESPONSE'))

__personas_data = PersonasData()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def __handle_unauthorized(response: Response, message: str) -> BaseResponse:
    response.status_code = 401
    return fail_response(message)

def __handle_bad_request(response: Response, message: str) -> BaseResponse:
    response.status_code = 400
    return fail_response(message)

@app.post('/generate-id')
def generate_id(response: Response) -> BaseResponse:
    try:
        id = generate_random_id()

        return BaseResponse(
            success=True,
            source=id
        )
    except Exception as e:
        return __handle_bad_request(
            response=response,
            message=f'Fail to generate the ID: {e}'
        )

@app.post('/talk/{id}/{persona_id}')
def talk_with_persona(id: str, persona_id: int, talk_request: TalkRequest, response: Response) -> BaseResponse:
    try:
        persona = __personas_data.get_by_id(persona_id)

        history = HistoryConversation(id, persona.id())
        messages_history = history.get_history(limit=__limit_messages_to_persona)

        history.append_human_conversation(talk_request.message)

        persona_message = ''
        for answer in talk(persona.prompt(), talk_request.message, messages_history):
            persona_message += answer

        history.append_bot_conversation(persona_message)

        return persona_message_to_response(persona_message)
    except Exception as e:
        return __handle_bad_request(
            response=response,
            message=f'Fail to talk with the persona: {e}'
        )

@app.get('/messages/{id}/{persona_id}')
def get_messages(id: str, persona_id: int, response: Response) -> BaseResponse:
    try:
        persona = __personas_data.get_by_id(persona_id)

        history = HistoryConversation(id, persona.id())
        messages_history = history.get_history(limit=__limit_messages_to_response)

        return messages_history_to_response(messages_history)
    except Exception as e:
        return __handle_bad_request(
            response=response,
            message=f'Fail to get the history messages: {e}'
        )

@app.get('/personas')
def get_personas(response: Response):
    try:
        personas = __personas_data.get_all()
        return personas_list_to_response(personas)
    except Exception as e:
        return __handle_bad_request(
            response=response,
            message=f'Fail to get the personas: {e}'
        )
    
@app.get('/persona/{id}')
def get_personas(id: int, response: Response):
    try:
        persona = __personas_data.get_by_id(id)
        return persona_to_response(persona)
    except Exception as e:
        return __handle_bad_request(
            response=response,
            message=f'Fail to get the personas: {e}'
        )

@app.post('/persona')
def create_persona(persona_request: PersonaRequest, request: Request, response: Response) -> BaseResponse:
    try:
        secret_key = request.headers.get("X-Secret-Key")
        if not validate_secret_key(secret_key):
            return __handle_unauthorized(
                response=response,
                message=f'Access unauthorized'
            )

        persona_created = __personas_data.include_persona(
            name=persona_request.name,
            prompt=persona_request.prompt
        )

        return persona_to_response(persona_created)
    except Exception as e:
        return __handle_bad_request(
            response=response,
            message=f'Fail to create a new persona: {e}'
        )
    
@app.put('/persona/{id}')
def update_persona(id: int, persona_request: PersonaRequest, request: Request, response: Response) -> BaseResponse:
    try:
        secret_key = request.headers.get("X-Secret-Key")
        if not validate_secret_key(secret_key):
            return __handle_unauthorized(
                response=response,
                message=f'Access unauthorized'
            )
        
        persona_updated = __personas_data.update_persona(
            id=id,
            name=persona_request.name,
            prompt=persona_request.prompt
        )
        if not persona_updated:
            return fail_response('Persona not found.')

        return persona_to_response(persona_updated)
    except Exception as e:
        return __handle_bad_request(
            response=response,
            message=f'Fail to update the persona: {e}'
        )

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, log_level='debug')