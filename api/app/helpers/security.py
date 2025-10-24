from functools import wraps
import inspect
import os
import uuid

from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import HTTPException, Request, Response

from app.infra.repository import Repository


load_dotenv()

__session_id: str | None = None

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

def handle_generated_id(request: Request) -> IdGenerated:
    if not request:
        raise HTTPException(status_code=500, detail="Request not found")
    
    session_id_header = request.headers.get("X-Session-ID")
    if not session_id_header:
        raise HTTPException(status_code=401, detail="X-Session-ID header required")
    
    try:
        id_generated = get_generated_id(session_id_header)
        if not id_generated:
            raise HTTPException(status_code=401, detail="Session not found")

        if id_generated.is_session_expired():
            raise HTTPException(status_code=401, detail="Session expired")
        
        return id_generated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid session ID: {str(e)}")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session validation error: {str(e)}")

def generate_random_id() -> IdGenerated:
    id_generated = IdGenerated()
    id_generated.generate_id()

    repo = Repository()
    repo.connect()

    repo.insert(str(id_generated.id()), id_generated.expires_in())

    return id_generated

def get_generated_id(id: str) -> IdGenerated | None:
    repo = Repository()
    repo.connect()

    expires_in = repo.get(id)
    if not expires_in:
        return None

    return IdGenerated(
        id=id,
        expires_in=int(expires_in)
    )

def validate_secret_key(secret_to_validate: str) -> bool:
    api_secret = os.getenv('API_SECRET')
    return api_secret == secret_to_validate

def session_validator(func):
    @wraps(func)
    def validate_session(*args, **kwargs):
        request = None
        
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        for _, param_value in bound_args.arguments.items():
            if isinstance(param_value, Request):
                request = param_value
                break
        
        if not request:
            raise HTTPException(status_code=500, detail="Request not found")
        
        id_generated = handle_generated_id(request)
        global __session_id
        __session_id = str(id_generated.id())
        
        try:
            if inspect.iscoroutinefunction(func):
                return func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
                return result
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            raise
    
    return validate_session

def api_secret_validator(func):
    @wraps(func)
    def validate_secret(*args, **kwargs):
        
        from app.controllers.base_controller import handle_unauthorized
        
        request = None
        response = None
        
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        for _, param_value in bound_args.arguments.items():
            if isinstance(param_value, Request):
                request = param_value
            elif isinstance(param_value, Response):
                response = param_value

            if request and response:
                break
        
        if not request:
            raise HTTPException(status_code=500, detail="Request not found")
        elif not response:
            raise HTTPException(status_code=500, detail="Response not found")
        
        secret_key = request.headers.get("X-Secret-Key")
        if not validate_secret_key(secret_key):
            return handle_unauthorized(
                response=response,
                message=f'Access unauthorized'
            )
        
        try:
            if inspect.iscoroutinefunction(func):
                return func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
                return result
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            raise

    return validate_secret

def api_secret_validator_async(func):
    @wraps(func)
    async def validate_secret(*args, **kwargs):
        from app.controllers.base_controller import handle_unauthorized
        
        request = None
        response = None
        
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        for _, param_value in bound_args.arguments.items():
            if isinstance(param_value, Request):
                request = param_value
            elif isinstance(param_value, Response):
                response = param_value

            if request and response:
                break
        
        if not request:
            raise HTTPException(status_code=500, detail="Request not found")
        elif not response:
            raise HTTPException(status_code=500, detail="Response not found")
        
        secret_key = request.headers.get("X-Secret-Key")
        if not validate_secret_key(secret_key):
            return handle_unauthorized(
                response=response,
                message=f'Access unauthorized'
            )
        
        try:
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
                return result
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            raise

    return validate_secret

def get_session_id():
    global __session_id
    return __session_id
