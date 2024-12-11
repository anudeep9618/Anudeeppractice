import asyncio

from fastapi.responses import JSONResponse
import httpx
from fastapi import HTTPException, status
from pydantic import ValidationError
from vzLog import vzLog
from models.KirkeAccessTokenResponse import KirkeAccessTokenResponse 
from models.KirkeJwtTokenResponse import KirkeJwtTokenResponse 
from models.CreateKirkeRequestPayload import CreateKirkeRequestPayload 
from models.CreateKirkeResponsePayload import CreateKirkeResponsePayload
from models.GetKirkeResponsePayload import GetKirkeResponsePayload
from models.GetLocationResponsePayload import GetLocationResponsePayload

class Kirke:
    def __init__(self):
        # self.base_url = "http://localhost:8100";
        self.base_url = "https://oa-uat.ebiz.verizon.com";
        self.access_token_url = "/oauth/client_credential/accesstoken?grant_type=client_credentials"
        self.jwt_token_url = "/msjv-kirke-changemanagement/userAccessTokenInfo?username="
        self.jwt_token_username = "SVC-gxov_kirke_np"
        self.client_id = "wZpwWqjn23opEr2KZteBGriGbE21AC7r"
        self.client_secret = "qLqRQSJmmQAQJs5j"
        self.create_kirke_url = "/msjv-kirke-changemanagement/changerequests/v2"
        self.get_kirke_url = "/msjv-kirke-changemanagement/changerequests/"
        self.get_location_url = "/msjv-kirke-changemanagement/masterdata/location"


    async def get_access_token(self):
        vzLog.log_debug("get access token started")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}{self.access_token_url}", headers=headers, data=data)

            vzLog.log_debug(f"Request url: {response.request.url}")
            vzLog.log_debug(f"Request method: {response.request.method}")
            vzLog.log_debug(f"Request headers: {response.request.headers}")
            vzLog.log_debug(f"Request content: {response.request.content}")

            vzLog.log_debug(f"Response status: {response.status_code}")
            vzLog.log_debug(f"Response headers: {response.headers}")
            vzLog.log_debug(f"Response content: {response.content}")

            # If not 200 it will raise exception
            response.raise_for_status()

            response_data = response.json()
            KirkeAccessTokenResponse.model_validate(response_data)

            vzLog.log_debug("get access token ended")
            return response_data["access_token"]

        except httpx.HTTPStatusError as e:
            vzLog.log_error(f"get_access_token api error, status_code={e.response.status_code}")
            vzLog.log_error(f"Exception:{str(e)}")
            return None
        except httpx.RequestError as e:
            vzLog.log_error(f"get_access_token api error, Network/Timeout/SSL issue")
            vzLog.log_error(f"Exception:{str(e)}")
        except ValidationError as e:
            vzLog.log_error(f"get_access_token api error, response data validation error, payload={response_data}")
            vzLog.log_error(f"Exception:{str(e)}")
        finally:
            if client:
                await client.aclose()
                vzLog.log_debug("httpx client connection closed")

    async def get_jwt_token(self):
        vzLog.log_debug("get jwt token started")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}{self.jwt_token_url}{self.jwt_token_username}")
            
            vzLog.log_debug(f"Request url: {response.request.url}")
            vzLog.log_debug(f"Request method: {response.request.method}")
            vzLog.log_debug(f"Request headers: {response.request.headers}")
            vzLog.log_debug(f"Request content: {response.request.content}")

            vzLog.log_debug(f"Response status: {response.status_code}")
            vzLog.log_debug(f"Response headers: {response.headers}")
            vzLog.log_debug(f"Response content: {response.content}")
			
			 # If not 200 it will raise exception
            response.raise_for_status()

            response_data = response.json()
            KirkeJwtTokenResponse.model_validate(response_data)

            vzLog.log_debug("get jwt token ended")
            return response_data["jwtToken"]

        except httpx.HTTPStatusError as e:
            vzLog.log_error(f"get_jwt_token api error, status_code={e.response.status_code}")
            vzLog.log_error(f"Exception:{str(e)}")
        except httpx.RequestError as e:
            vzLog.log_error(f"get_jwt_token api error, Network/Timeout/SSL issue")
            vzLog.log_error(f"Exception:{str(e)}")
        except ValidationError as e:
            vzLog.log_error(f"get_jwt_token api error, response data validation error, payload={response_data}")
            vzLog.log_error(f"Exception:{str(e)}")
        finally:
            if client:
                await client.aclose()
                vzLog.log_debug("httpx client connection closed")

    async def create_api(self, authorization : str, jwt_token : str, create_kirke_request_payload : CreateKirkeRequestPayload):
        vzLog.log_debug("create api started")
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
            "Authorization": f"Bearer {authorization}",
            "jwtToken": jwt_token,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}{self.create_kirke_url}", headers=headers, json=create_kirke_request_payload.model_dump(by_alias=True)
                )

            vzLog.log_debug(f"Request url: {response.request.url}")
            vzLog.log_debug(f"Request method: {response.request.method}")
            vzLog.log_debug(f"Request headers: {response.request.headers}")
            vzLog.log_debug(f"Request content: {response.request.content}")

            vzLog.log_debug(f"Response status: {response.status_code}")
            vzLog.log_debug(f"Response headers: {response.headers}")
            vzLog.log_debug(f"Response content: {response.content}")

            # If not 200 it will raise exception
            response.raise_for_status()

            # Parse and validate response
            response_data = response.json()
            vzLog.log_debug("create api ended")
            return CreateKirkeResponsePayload.model_validate(response_data)

        except httpx.HTTPStatusError as e:
            vzLog.log_error(f"create_kirke_api error, status_code={e.response.status_code}")
            vzLog.log_error(f"Exception:{str(e)}")
        except httpx.RequestError as e:
            vzLog.log_error(f"create_kirke_api error, Network/Timeout/SSL issue")
            vzLog.log_error(f"Exception:{str(e)}")
        except ValidationError as e:
            vzLog.log_error(f"create_kirke_api error, response data validation error, payload={response_data}")
            vzLog.log_error(f"Exception:{str(e)}")
        finally:
            if client:
                await client.aclose()
                vzLog.log_debug("httpx client connection closed") 

    # def close_api(self, api_id):
    #     response = requests.delete(f"{self.base_url}{Config.CLOSE_API_ENDPOINT}/{api_id}")
    #     return response.json()

    async def create_kirke(self, create_kirke_request_payload: CreateKirkeRequestPayload):
        vzLog.log_debug("create kirke started")
        try:
            access_token_api_task = asyncio.create_task(self.get_access_token())
            jwt_token_api_task = asyncio.create_task(self.get_jwt_token())

            access_token, jwt_token = await asyncio.gather(access_token_api_task, jwt_token_api_task)

            vzLog.log_debug("create kirke ended")
            if access_token is not None and jwt_token is not None:
                create_kirke_response = await self.create_api(access_token, jwt_token, create_kirke_request_payload)
                if create_kirke_response is not None:
                    return create_kirke_response
                else:
                    return None
            else:
                return None
        except Exception as e:
            vzLog.log_error(f"create_kirke method failed")
            return None
			
			
			async def get_api(self, authorization : str, jwt_token : str, request_id : int):
        vzLog.log_debug("get api started")
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
            "Authorization": f"Bearer {authorization}",
            "jwtToken": jwt_token,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}{self.get_kirke_url}{request_id}", headers=headers
                )

            vzLog.log_debug(f"Request url: {response.request.url}")
            vzLog.log_debug(f"Request method: {response.request.method}")
            vzLog.log_debug(f"Request headers: {response.request.headers}")
            vzLog.log_debug(f"Request content: {response.request.content}")

            vzLog.log_debug(f"Response status: {response.status_code}")
            vzLog.log_debug(f"Response headers: {response.headers}")
            vzLog.log_debug(f"Response content: {response.content}")


            # If not 200 it will raise exception
            response.raise_for_status()
            # Parse and validate response
            response_data = response.json()
            vzLog.log_debug("get api ended")
            return GetKirkeResponsePayload.model_validate(response_data)

        except httpx.HTTPStatusError as e:
            vzLog.log_error(f"get_kirke_api error, status_code={e.response.status_code}")
            vzLog.log_error(f"Exception:{str(e)}")
        except httpx.RequestError as e:
            vzLog.log_error(f"get_kirke_api error, Network/Timeout/SSL issue")
            vzLog.log_error(f"Exception:{str(e)}")
        except ValidationError as e:
            vzLog.log_error(f"get_kirke_api error, response data validation error, payload={response_data}")
            vzLog.log_error(f"Exception:{str(e)}")
        finally:
            if client:
                await client.aclose()
                vzLog.log_debug("httpx client connection closed") 

    # def close_api(self, api_id):
    #     response = requests.delete(f"{self.base_url}{Config.CLOSE_API_ENDPOINT}/{api_id}")
    #     return response.json()

    async def get_kirke(self, request_id : int):
        vzLog.log_debug("get kirke started")
        try:
            access_token_api_task = asyncio.create_task(self.get_access_token())
            jwt_token_api_task = asyncio.create_task(self.get_jwt_token())

            access_token, jwt_token = await asyncio.gather(access_token_api_task, jwt_token_api_task)

            vzLog.log_debug("get kirke ended")
            if access_token is not None and jwt_token is not None:
                get_kirke_response = await self.get_api(access_token, jwt_token, request_id)
                if get_kirke_response is not None:
                    return get_kirke_response
                else:
                    return None
            else:
                return None
        except Exception as e:
            vzLog.log_error(f"get_kirke method failed")
            return None
			
			async def get_location_api(self, authorization : str, jwt_token : str, state: str, city: str, country:str, page:int):
        vzLog.log_debug("get location api started")
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
            "Authorization": f"Bearer {authorization}",
            "jwtToken": jwt_token,
        }
        params = {
            "state": state,
            "city": city,
            "country": country,
            "page": page,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}{self.get_location_url}", headers=headers, params=params
                )

            vzLog.log_debug(f"Request url: {response.request.url}")
            vzLog.log_debug(f"Request method: {response.request.method}")
            vzLog.log_debug(f"Request headers: {response.request.headers}")
            vzLog.log_debug(f"Request content: {response.request.content}")

            vzLog.log_debug(f"Response status: {response.status_code}")
            vzLog.log_debug(f"Response headers: {response.headers}")
            vzLog.log_debug(f"Response content: {response.content}")

            # If not 200 it will raise exception
            response.raise_for_status()
            # Parse and validate response
            response_data = response.json()
            vzLog.log_debug("get location api ended")
            return GetLocationResponsePayload.model_validate(response_data)

        except httpx.HTTPStatusError as e:
            vzLog.log_error(f"get_location_api error, status_code={e.response.status_code}")
            vzLog.log_error(f"Exception:{str(e)}")
        except httpx.RequestError as e:
            vzLog.log_error(f"get_location_api error, Network/Timeout/SSL issue")
            vzLog.log_error(f"Exception:{str(e)}")
        except ValidationError as e:
            vzLog.log_error(f"get_location_api error, response data validation error, payload={response_data}")
            vzLog.log_error(f"Exception:{str(e)}")
        finally:
            if client:
                await client.aclose()
                vzLog.log_debug("httpx client connection closed") 

    # def close_api(self, api_id):
    #     response = requests.delete(f"{self.base_url}{Config.CLOSE_API_ENDPOINT}/{api_id}")
    #     return response.json()

    async def get_location(self, state: str, city: str, country:str, page:int):
        vzLog.log_debug("get location started")
        try:
            access_token_api_task = asyncio.create_task(self.get_access_token())
            jwt_token_api_task = asyncio.create_task(self.get_jwt_token())

            access_token, jwt_token = await asyncio.gather(access_token_api_task, jwt_token_api_task)

            vzLog.log_debug("get location ended")
            if access_token is not None and jwt_token is not None:
                get_location_response = await self.get_location_api(access_token, jwt_token, state, city, country, page)
                if get_location_response is not None:
                    return get_location_response
                else:
                    return None
            else:
                return None
        except Exception as e:
            vzLog.log_error(f"get_kirke location method failed")
            return None