import asyncio

from fastapi.responses import JSONResponse
import httpx
from fastapi import HTTPException, status
from vzLog import vzLog
from models.AccessTokenRequestPayload import AccessTokenRequestPayload
from models.AccessTokenResponsePayload import AccessTokenResponsePayload

class TokenService:
    def __init__(self):
        self.VALID_CLIENT_ID = "svc-vsop-sa"
        self.VALID_CLIENT_SECRET = "sdfdsgsdadsgeaga"

        self.TOKEN = "kfWAjL1wCVFdJCY3BrDLrUESUWKN"

    async def validate_creds_and_get_token(self, access_token_request_payload: AccessTokenRequestPayload):
        # Replace hardcoded credentials with environment variables or config variables
        # Validate credentials
        if access_token_request_payload.client_id != self.VALID_CLIENT_ID or access_token_request_payload.client_secret != self.VALID_CLIENT_SECRET:
            vzLog.log_error("Authentication failed")
            return None
        else:
            return AccessTokenResponsePayload(token=self.TOKEN)
    
    async def validate_token(self, token: str):
        # Replace hardcoded credentials with environment variables or config variables
        # Validate credentials
        if token != self.TOKEN:
            vzLog.log_error("Token is invalid")
            return False
        else:
            return True