import json
from dataclasses import dataclass

from fastapi import status
from fastapi.responses import JSONResponse
from vzLog import vzLog

from models.FailureResponse import FailureResponse
from models.CreateKirkeRequestPayload import CreateKirkeRequestPayload
from services.TokenService import TokenService
from services.Kirke import Kirke
from models.AccessTokenResponsePayload import AccessTokenResponsePayload
from models.AccessTokenRequestPayload import AccessTokenRequestPayload


class RequestHandlers:
    proxies = None

    def __init__(self):
        self.kirke_service = Kirke()
        self.token_service = TokenService()

    async def handle_create_kirke(self, create_kirke_request_payload : CreateKirkeRequestPayload):
        try:
            vzLog.log_info("create kirke started")

            createKirkeResponsePayload = await self.kirke_service.create_kirke(create_kirke_request_payload)
            vzLog.log_info("create kirke completed")
            if createKirkeResponsePayload is not None:
                return JSONResponse(
                    content=createKirkeResponsePayload.model_dump(),
                    media_type="application/json",
                    status_code=status.HTTP_200_OK,
                )
            else:
                return JSONResponse(
                    content=FailureResponse(message = "create_kirke method failed", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR).model_dump(),
                    media_type="application/json",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        except Exception as e:
            vzLog.log_error(
                f"Error processing create_kirke, for payload: " + str(create_kirke_request_payload)
            )
            vzLog.log_error(str(e))
            vzLog.log_info("create kirke process failed")
            return JSONResponse(
                content=FailureResponse("create_kirke method failed").model_dump(),
                media_type="application/json",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def handle_get_kirke(self, request_id : int):
        try:
            vzLog.log_info("get kirke started")

            getKirkeResponsePayload = await self.kirke_service.get_kirke(request_id)
            vzLog.log_info("get kirke completed")
            if getKirkeResponsePayload is not None:
                return JSONResponse(
                    content=getKirkeResponsePayload.model_dump(),
                    media_type="application/json",
                    status_code=status.HTTP_200_OK,
                )
            else:
                return JSONResponse(
                    content=FailureResponse(message = "get_kirke method failed", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR).model_dump(),
                    media_type="application/json",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        except Exception as e:
            vzLog.log_error(
                f"Error processing get_kirke, for request: " + request_id
            )
            vzLog.log_error(str(e))
            vzLog.log_info("get kirke process failed")
            return JSONResponse(
                content=FailureResponse("get_kirke method failed").model_dump(),
                media_type="application/json",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
			
			async def handle_get_location(self, state: str, city: str, country:str, page:int):
        try:
            vzLog.log_info("get location started")

            getLocationResponsePayload = await self.kirke_service.get_location(state, city, country, page)
            vzLog.log_info("get location completed")
            if getLocationResponsePayload is not None:
                return JSONResponse(
                    content=getLocationResponsePayload.model_dump(),
                    media_type="application/json",
                    status_code=status.HTTP_200_OK,
                )
            else:
                return JSONResponse(
                    content=FailureResponse(message = "get location method failed", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR).model_dump(),
                    media_type="application/json",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        except Exception as e:
            vzLog.log_error(
                f"Error processing get location, for request: " + state, city, country, page
            )
            vzLog.log_error(str(e))
            vzLog.log_info("get location process failed")
            return JSONResponse(
                content=FailureResponse("get location method failed").model_dump(),
                media_type="application/json",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    async def handle_access_token(self, access_token_request_payload: AccessTokenRequestPayload):
        try:
            vzLog.log_info("access_token request started")
            accessTokenResponsePayload = await self.token_service.validate_creds_and_get_token(access_token_request_payload)
            vzLog.log_info("access_token request completed")
            if accessTokenResponsePayload is not None:
                return JSONResponse(
                    content=accessTokenResponsePayload.model_dump(),
                    media_type="application/json",
                    status_code=status.HTTP_200_OK,
                )
            else:
                return JSONResponse(
                    content=FailureResponse(message = "Authentication failed", status_code = status.HTTP_401_UNAUTHORIZED).model_dump(),
                    media_type="application/json",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
        except Exception as e:
            vzLog.log_error(
                f"Error processing access_token request, for payload: " + str(access_token_request_payload)
            )
            vzLog.log_error(str(e))
            vzLog.log_info("access_token request process failed")
            return JSONResponse(
                content=FailureResponse("access_token request method failed").model_dump(),
                media_type="application/json",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def handle_validate_token(self, token: str):
        try:
            vzLog.log_info("validating token started")
            validated = await self.token_service.validate_token(token)
            vzLog.log_info("validating token completed")
            return validated
        except Exception as e:
            vzLog.log_error(
                f"Error processing token validation, provided token: " + token
            )
            vzLog.log_error(str(e))
            vzLog.log_info("token validation process failed")
            return False