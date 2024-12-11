from fastapi import status
from pydantic import BaseModel

class FailureResponse(BaseModel):
    message: str
    status_code: int