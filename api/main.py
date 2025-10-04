# import threading
# import time

from brain import talk
from history_conversation import HistoryConversation
# from interface import InterfaceChat
from persona import PersonasData
# from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from talk_request import TalkRequest


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/talk")
def talk_with_persona(talk_request: TalkRequest):
    persona_data = PersonasData()
    persona = persona_data.get_personas()[0]

    persona_message = ''
    for answer in talk(persona.prompt(), talk_request.message, ''):
        persona_message += answer

    return { "persona_response": persona_message }

# __history = HistoryConversation()
# __persona_data = PersonasData()
# __persona = __persona_data.get_personas()[0]

# def start_conversation(interface: InterfaceChat):
#     interface.start_chat()
#     message = interface.write_user_message()

#     def process_in_background():
#         time.sleep(.7)
#         interface.set_bot_as_thinking()

#         messages_history = __history.get_history()
#         __history.append_human_conversation(message)

#         persona_message = ''
#         for answer in talk(__persona.prompt(), message, messages_history):
#             interface.write_bot_message(answer)
#             persona_message += answer

#         __history.append_bot_conversation(persona_message)

#         interface.finish_chat_bot_message()
#         interface.finish_chat()

#     thread = threading.Thread(target=process_in_background)
#     thread.daemon = True
#     thread.start()

# if __name__ == '__main__':
#     interface = InterfaceChat(
#         character_name=__persona.name(),
#         waiting_message='Aguarde...',
#         action_button=start_conversation,
#     )
#     interface.run()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="debug")