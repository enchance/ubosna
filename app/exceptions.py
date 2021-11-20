from typing import Optional, Any, Dict
from fastapi import HTTPException, status

from app import settings as s

"""
200: Successful request
201: Successful creation
204: Successful update or delete; nothing needs to be returned
400: I don't understand the data so I don't know what to do
422: I understand it but am not allowing it (non-unique, blocked data, etc.)
403: No permission; you can't do that it's bad and you should feel bad
503: Your db exploded, server burned down or something
"""
OK_200 = 200            # Read
CREATED_201 = 201       # Create
NO_CONTENT_204 = 204    # Update, Delete
GENERIC_400 = 400
UNPROCESSABLE_422 = 422
FORBIDDEN_NO_PERM_403 = 403
SERVICE_UNAVAILABLE_503 = 503


class BaseAppError(HTTPException):
    message = 'UNABLE TO CONTINUE'
    status_code = GENERIC_400

    def __init__(self, detail: Optional[Any] = None, status_code: Optional[int] = None,
                 *, headers: Optional[Dict[str, Any]] = None) -> None:
        detail = detail or self.message
        status_code = status_code or self.status_code
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class GenericError(BaseAppError):
    """I don't understand what you're trying to do."""
    pass

    
class FalsyDataError(BaseAppError):
    """Data is falsy such as '', [], None, {}, set(), False, etc.."""
    message = "FALSY OR None data supplied"
    status_code = UNPROCESSABLE_422


class ServiceError(BaseAppError):
    """Unable to continue because a service is down (e.g. database)."""
    message = 'SERVICE UNAVAILABLE'
    status_code = SERVICE_UNAVAILABLE_503


class PermissionDenied(BaseAppError):
    """User doesn't have permission to do something."""
    message = "YOU'RE NOT ALLOWED TO DO THAT"
    status_code = FORBIDDEN_NO_PERM_403


class NotFoundError(BaseAppError):
    message = "DATA NOT FOUND"
    # Not 404 since pov is from the client (422) not the app (404)
    status_code = GENERIC_400
    
    def __init__(self, model: str = None):
        message = s.DEBUG and model and f'{model} not found' or self.message
        super().__init__(message)