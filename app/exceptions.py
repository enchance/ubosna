from fastapi import HTTPException
from typing import Optional, Any, Dict


GENERIC_422 = 422
PERMISSION_DENIED_403 = 403
SERVICE_UNAVAILABLE_503 = 503


class BaseAppError(HTTPException):
    message = 'NO MESSAGE INCLUDED'
    status_code = GENERIC_422

    def __init__(self, detail: Optional[Any] = None, status_code: Optional[int] = None,
                 *, headers: Optional[Dict[str, Any]] = None) -> None:
        detail = detail or self.message
        status_code = status_code or self.status_code
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class FalsyDataError(BaseAppError):
    """Data is falsy such as '', [], None, {}, set(), False, etc.."""
    message = "FALSY DATA OR NONE"
    status_code = GENERIC_422


class ServiceError(BaseAppError):
    """Unable to continue work because of a service error (e.g. database)."""
    message = 'UNABLE TO PROCESS DATA'
    status_code = SERVICE_UNAVAILABLE_503


class PermissionDenied(BaseAppError):
    """User doesn't have permission to do something."""
    message = 'INSUFFICIENT PERMISSIONS'
    status_code = PERMISSION_DENIED_403


class NotFoundError(BaseAppError):
    message = "DATA NOT FOUND"
    # Not 404 since pov is from the client (422) not the app (404)
    status_code = GENERIC_422
    
    def __init__(self, model: str = None):
        message = s.DEBUG and model and f'{model} not found' or self.message
        super().__init__(message)