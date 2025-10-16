from datetime import datetime, timedelta
import os
import uuid

from dotenv import load_dotenv


load_dotenv()

class IdGenerated:
    def __init__(self, id = None, expires_in = None):
        self.__id = id
        self.__expires_in = expires_in

    def __calculate_expire_id(self) -> int:
        days_limit = int(os.getenv('ID_EXPIRES_IN_DAYS'))
        expire_time = datetime.now() + timedelta(days=days_limit)
        return int(expire_time.timestamp())

    def generate_id(self):
        self.__id = uuid.uuid4()
        self.__expires_in = self.__calculate_expire_id()

    def id(self) -> uuid.UUID:
        return self.__id
    
    def expires_in(self) -> int:
        return self.__expires_in
    
    def is_session_expired(self) -> bool:
        current_timestamp = int(datetime.now().timestamp())
        return current_timestamp > self.__expires_in

def generate_random_id() -> IdGenerated:
    id_generated = IdGenerated()
    id_generated.generate_id()

    return id_generated

def validate_secret_key(secret_to_validate: str) -> bool:
    api_secret = os.getenv('API_SECRET')
    return api_secret == secret_to_validate
