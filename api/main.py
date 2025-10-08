from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from brain import talk
from history_conversation import HistoryConversation
from persona import PersonasData
from talk_request import TalkRequest


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
    persona_data = PersonasData()
    persona = persona_data.get_by_id(persona_id)

    history = HistoryConversation(ip, persona.id())
    previous_conversation = '\n'.join(history.get_history())

    history.append_human_conversation(talk_request.message)

    persona_message = ''
    for answer in talk(persona.prompt(), talk_request.message, previous_conversation):
        persona_message += answer

    history.append_bot_conversation(persona_message)

    return { 'persona_response': persona_message }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, log_level='debug')