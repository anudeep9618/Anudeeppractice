from pydantic import BaseModel
from typing import List


class KirkeJwtTokenResponse(BaseModel):
    refresh_token_expires_in: str
    api_product_list: str
    api_product_list_json: List[str]
    organization_name: str
    token_type: str
    issued_at: str
    access_token: str
    application_name: str
    scope: str
    expires_in: str
    refresh_count: str
    status: str
    jwtToken: str