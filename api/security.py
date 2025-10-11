import os
import uuid

from dotenv import load_dotenv


def generate_random_id():
    return uuid.uuid4()

def validate_secret_key(secret_to_validate: str) -> bool:
    load_dotenv()

    api_secret = os.getenv('API_SECRET')
    return api_secret == secret_to_validate