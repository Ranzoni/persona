from fastapi import APIRouter, Response

from app.helpers.mappers import fail_response, id_generated_to_response
from app.helpers.security import generate_random_id
from app.infra.personas_data import PersonasData
from app.models.api_models import BaseResponse


router = APIRouter()

__personas_data = PersonasData()

def handle_unauthorized(response: Response, message: str) -> BaseResponse:
    response.status_code = 401
    return fail_response(message)

def handle_bad_request(response: Response, message: str) -> BaseResponse:
    response.status_code = 400
    return fail_response(message)

def handle_not_found_request(response: Response, message: str) -> BaseResponse:
    response.status_code = 404
    return fail_response(message)

def handle_conflict_request(response: Response, message: str) -> BaseResponse:
    response.status_code = 409
    return fail_response(message)

@router.post('/generate-id')
def generate_id(response: Response) -> BaseResponse:
    try:
        id_generated = generate_random_id()

        return id_generated_to_response(id_generated)
    except Exception as e:
        return handle_bad_request(
            response=response,
            message=f'Fail to generate the ID: {e}'
        )
    
def get_personas_data() -> PersonasData:
    return __personas_data
