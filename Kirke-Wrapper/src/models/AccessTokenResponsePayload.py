from typing import Optional, Any, List, Dict

from pydantic import BaseModel


class AccessTokenResponsePayload(BaseModel):
    token: str