from typing import Optional, Any, List

from pydantic import BaseModel


class AccessTokenRequestPayload(BaseModel):
    client_id: str
    client_secret: str