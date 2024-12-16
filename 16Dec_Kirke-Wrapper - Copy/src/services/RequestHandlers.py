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
from models.GetDeviceResponsePayload import GetDeviceResponsePayload


class RequestHandlers:
    proxies = None

    def __init__(self):
        self.kirke_service = Kirke()
        self.token_service = TokenService()

    async def handle_create_kirke(self, create_kirke_request_payload : CreateKirkeRequestPayload):
        try:
            vzLog.log_info("create kirke started")

            createKirkeResponsePayload = await self.kirke_service.create_kirke(create_kirke_request_payload)
            #vzLog.log_info("create kirke completed")
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

    async def handle_get_kirke_status(self, request_id: int):
        try:
            vzLog.log_info("get kirke status started")
            get_kirke_status_response = await self.kirke_service.get_kirke_status(request_id)
            vzLog.log_info("get kirke status completed")
            if get_kirke_status_response is not None:
                return JSONResponse(
                    content=get_kirke_status_response,  # Forward JSON directly
                    media_type="application/json",
                    status_code=200,
                )
            else:
                return JSONResponse(
                    content={"message": "get_kirke_status method failed", "status_code": 500},
                    media_type="application/json",
                    status_code=500,
                )
        except Exception as e:
            vzLog.log_error(f"Error processing get_kirke_status for request: {request_id}")
            vzLog.log_error(str(e))
            vzLog.log_info("get kirke status process failed")
            return JSONResponse(
                content={"message": "get_kirke_status method failed", "status_code": 500},
                media_type="application/json",
                status_code=500,
            )

    async def handle_withdraw_kirke_request(self, request_id: int, on_behalf_of: str, authorization: str, jwt_token: str):
        try:
            vzLog.log_info(f"Withdraw kirke request started for {request_id} by {on_behalf_of}")

            response = await self.kirke_service.withdraw_request(request_id, on_behalf_of)
            vzLog.log_info("Withdraw kirke request completed")
            if response:
                return JSONResponse(
                    content=response,
                    media_type="application/json",
                    status_code=200,
                )
            else:
                return JSONResponse(
                    content={"message": "Withdraw request failed", "status_code": 500},
                    media_type="application/json",
                    status_code=500,
                )
        except Exception as e:
            vzLog.log_error(f"Error processing withdraw_kirke_request for {request_id}")
            vzLog.log_error(str(e))
            vzLog.log_info("Withdraw kirke request process failed")
            return JSONResponse(
                content={"message": "Withdraw request failed", "status_code": 500},
                media_type="application/json",
                status_code=500,
            )

    async def handle_get_device(self, device_name : str, start_date_time : str,
                                end_date_time : str, start_date_offset : str, end_date_offset : str):
        try:
            vzLog.log_info("get device started")

            getdeviceResponsePayload = await self.kirke_service.get_device(device_name, start_date_time, end_date_time, start_date_offset, end_date_offset)
            
            vzLog.log_info("get device completed")
            if getdeviceResponsePayload is not None:
                return JSONResponse(
                    content=getdeviceResponsePayload,
                    media_type="application/json",
                    status_code=status.HTTP_200_OK,
                )
            else:
                return JSONResponse(
                    content=FailureResponse(message = "get_device method failed", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR).model_dump(),
                    media_type="application/json",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        except Exception as e:
            vzLog.log_error(
                f"Error processing get_device, for device name: " + device_name
            )
            vzLog.log_error(str(e))
            vzLog.log_info("get device process failed")
            return JSONResponse(
                content=FailureResponse("get_device method failed").model_dump(),
                media_type="application/json",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
