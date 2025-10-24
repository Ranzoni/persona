from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import base_controller, messages_controller, personas_controller, talk_controller
from app.services.image import get_upload_dir


load_dotenv()

__allow_origins = os.getenv('ALLOW_ORIGINS')
__allow_credentials = bool(os.getenv('ALLOW_CREDENTIALS'))

app = FastAPI()

app.include_router(base_controller.router, prefix="/api")
app.include_router(personas_controller.router, prefix="/api/persona")
app.include_router(messages_controller.router, prefix="/api/message")
app.include_router(talk_controller.router, prefix="/api/talk")

@app.get("/")
async def root():
    return {"message": "Persona API"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=__allow_origins.split(','),
    allow_credentials=__allow_credentials,
    allow_methods=['*'],
    allow_headers=['*'],
)

os.makedirs(get_upload_dir(), exist_ok=True)

app.mount('/images', StaticFiles(directory=get_upload_dir()), name='images')

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, log_level='debug')