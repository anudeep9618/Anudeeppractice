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
from models.GetDeviceResponsePayload import GetDeviceResponsePayload

class Kirke:
    def __init__(self):
        self.base_url = "http://localhost:8100"
        # self.base_url = "https://oa-uat.ebiz.verizon.com"
        self.access_token_url = "/oauth/client_credential/accesstoken?grant_type=client_credentials"
        self.jwt_token_url = "/msjv-kirke-changemanagement/userAccessTokenInfo?username="
        self.jwt_token_username = "SVC-gxov_kirke_np"
        self.client_id = "wZpwWqjn23opEr2KZteBGriGbE21AC7r"
        self.client_secret = "qLqRQSJmmQAQJs5j"
        self.create_kirke_url = "/msjv-kirke-changemanagement/changerequests/v2"
        self.get_kirke_url = "/msjv-kirke-changemanagement/changerequests/"
        self.get_location_url = "/msjv-kirke-changemanagement/masterdata/location"
        self.get_device_url = "/msjv-kirke-changemanagement/devices"


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
            print("Exception######################################",e)
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


    async def get_kirke_status_api(self, authorization: str, jwt_token: str, request_id: int):
        vzLog.log_debug("get kirke status API started")
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {authorization}",
            "jwtToken": jwt_token,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}{self.get_kirke_url}{request_id}/status", headers=headers
                )

            vzLog.log_debug(f"Request URL: {response.request.url}")
            vzLog.log_debug(f"Response Status: {response.status_code}")
            vzLog.log_debug(f"Response Content: {response.content}")

            # If not 200, raise an exception
            response.raise_for_status()
            # Return raw JSON response
            vzLog.log_debug("get kirke status API ended")
            return response.json()

        except httpx.HTTPStatusError as e:
            vzLog.log_error(f"get_kirke_status_api error, status_code={e.response.status_code}")
            vzLog.log_error(f"Exception: {str(e)}")
        except httpx.RequestError as e:
            vzLog.log_error("get_kirke_status_api error: Network/Timeout/SSL issue")
            vzLog.log_error(f"Exception: {str(e)}")
        except Exception as e:
            vzLog.log_error("get_kirke_status_api error: Unexpected exception")
            vzLog.log_error(f"Exception: {str(e)}")
        finally:
            if client:
                await client.aclose()
                vzLog.log_debug("HTTPX client connection closed")

    async def get_kirke_status(self, request_id: int):
        vzLog.log_debug("get kirke status started")
        try:
            access_token_api_task = asyncio.create_task(self.get_access_token())
            jwt_token_api_task = asyncio.create_task(self.get_jwt_token())

            access_token, jwt_token = await asyncio.gather(access_token_api_task, jwt_token_api_task)

            if access_token is not None and jwt_token is not None:
                return await self.get_kirke_status_api(access_token, jwt_token, request_id)
            return None
        except Exception as e:
            vzLog.log_error("get_kirke_status method failed")
            return None
        

    async def withdraw_kirke_request(self, request_id: int, on_behalf_of: str, authorization: str, jwt_token: str):
        vzLog.log_debug(f"withdraw kirke request API started for {request_id} by {on_behalf_of}")
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
            "Authorization": f"Bearer {authorization}",
            "jwtToken": jwt_token,
        }
        params = {"on-behalf-of": on_behalf_of}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{self.base_url}{self.get_kirke_url}{request_id}/withdraw",
                    headers=headers,
                    params=params,
                )

            vzLog.log_debug(f"Request URL: {response.request.url}")
            vzLog.log_debug(f"Response Status: {response.status_code}")
            vzLog.log_debug(f"Response Content: {response.content}")

            # If not 200, raise exception
            response.raise_for_status()
            # Return raw JSON response
            vzLog.log_debug("withdraw kirke request API ended")
            return response.json()

        except httpx.HTTPStatusError as e:
            vzLog.log_error(f"withdraw_kirke_request API error, status_code={e.response.status_code}")
            vzLog.log_error(f"Exception: {str(e)}")
        except httpx.RequestError as e:
            vzLog.log_error("withdraw_kirke_request API error: Network/Timeout/SSL issue")
            vzLog.log_error(f"Exception: {str(e)}")
        except Exception as e:
            vzLog.log_error("withdraw_kirke_request API error: Unexpected exception")
            vzLog.log_error(f"Exception: {str(e)}")
        finally:
            if client:
                await client.aclose()
                vzLog.log_debug("HTTPX client connection closed")

    async def withdraw_request(self, request_id: int, on_behalf_of: str):
        vzLog.log_debug("withdraw kirke request API started")
        try:
            access_token_api_task = asyncio.create_task(self.get_access_token())
            jwt_token_api_task = asyncio.create_task(self.get_jwt_token())

            access_token, jwt_token = await asyncio.gather(access_token_api_task, jwt_token_api_task)

            vzLog.log_debug("withdraw kirke request API ended")
            if access_token is not None and jwt_token is not None:
                withdraw_request_response = await self.withdraw_kirke_request(request_id, on_behalf_of, access_token, jwt_token)
                if withdraw_request_response is not None:
                    return withdraw_request_response
                else:
                    return None
            else:
                return None
        except Exception as e:
            vzLog.log_error(f"withdraw kirke request API failed")
            return None


    async def get_device_api(self, authorization : str, jwt_token : str, device_name : str, start_date_time : str,
                             end_date_time : str, start_date_offset : str, end_date_offset : str):
        vzLog.log_debug("get api started")
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
            "Authorization": f"Bearer {authorization}",
            "jwtToken": jwt_token,
        }
        params = {
            "start_date_time" : start_date_time,
            "end_date_time" : end_date_time,
            "start_date_offset " : start_date_offset,
            "end_date_offset " : end_date_offset,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}{self.get_device_url}/{device_name}/changerequests", headers=headers, params=params
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
            vzLog.log_debug("get device api ended")
            return GetDeviceResponsePayload.model_validate(response_data)

        except httpx.HTTPStatusError as e:
            vzLog.log_error(f"get_device_api error, status_code={e.response.status_code}")
            vzLog.log_error(f"Exception:{str(e)}")
        except httpx.RequestError as e:
            vzLog.log_error(f"get_device_api error, Network/Timeout/SSL issue")
            vzLog.log_error(f"Exception:{str(e)}")
        except ValidationError as e:
            vzLog.log_error(f"get_device_api error, response data validation error, payload={response_data}")
            vzLog.log_error(f"Exception:{str(e)}")
        finally:
            if client:
                await client.aclose()
                vzLog.log_debug("httpx client connection closed") 

    async def get_device(self, device_name : str, start_date_time : str, end_date_time : str, start_date_offset : str, end_date_offset : str):
        vzLog.log_debug("get device started")
        try:
            access_token_api_task = asyncio.create_task(self.get_access_token())
            jwt_token_api_task = asyncio.create_task(self.get_jwt_token())

            access_token, jwt_token = await asyncio.gather(access_token_api_task, jwt_token_api_task)

            vzLog.log_debug("get device ended")
            if access_token is not None and jwt_token is not None:
                get_device_response = await self.get_device_api(access_token, jwt_token, device_name, start_date_time, end_date_time, start_date_offset, end_date_offset)
                if get_device_response is not None:
                    return get_device_response
                else:
                    return None
            else:
                return None
        except Exception as e:
            vzLog.log_error(f"get_device method failed")
            return None
