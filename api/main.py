import uvicorn
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from brain import talk
from history_conversation import HistoryConversation
from persona import PersonasData
from talk_request import TalkRequest


load_dotenv()
__limit_messages_to_persona = int(os.getenv('LIMIT_MESSAGES_TO_PERSONA'))
__limit_messages_to_response = int(os.getenv('LIMIT_MESSAGES_TO_RESPONSE'))

__persona_data = PersonasData()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post('/talk/{ip}/{persona_id}')
def talk_with_persona(ip: str, persona_id: int, talk_request: TalkRequest):
    persona = __persona_data.get_by_id(persona_id)

    history = HistoryConversation(ip, persona.id())
    messages_history = history.get_history(limit=__limit_messages_to_persona)

    history.append_human_conversation(talk_request.message)

    persona_message = ''
    for answer in talk(persona.prompt(), talk_request.message, messages_history):
        persona_message += answer

    history.append_bot_conversation(persona_message)

    return { 'persona_response': persona_message }

@app.get('/messages/{ip}/{persona_id}')
def get_messages(ip: str, persona_id: int):
    persona = __persona_data.get_by_id(persona_id)

    history = HistoryConversation(ip, persona.id())
    messages_history = history.get_history(limit=__limit_messages_to_response)

    messages_dict = [
        {
            'who': msg.get_who(),
            'content': msg.get_content()
        }
        for msg in messages_history
    ]

    return { 'history_messages': messages_dict }

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, log_level='debug')