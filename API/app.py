from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import httpx

app = FastAPI()

# Input model to validate request payload
class AccessTokenRequest(BaseModel):
    client_id: str
    client_secret: str

# Output model to structure the response payload
class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

# Input model to validate the username payload
# class UserAccessTokenInfoRequest(BaseModel):
#     username: str

# Output model to structure the response payload (adjust based on actual API response)
class UserAccessTokenInfoResponse(BaseModel):
    user_id: str
    roles: list[str]
    permissions: list[str]

# Input model for the request payload
class Location(BaseModel):
    location_id: int = Field(..., alias="location-id")

class OutageInfo(BaseModel):
    number_of_outages: int = Field(..., alias="number-of-outages")
    outage_duration: int = Field(..., alias="outage-duration")
    outage_unit_of_measure: str = Field(..., alias="outage-unit-of-measure")

class OutageDetails(BaseModel):
    outage_info: OutageInfo = Field(..., alias="outage-info")

class MOP(BaseModel):
    mop_url: str = Field(..., alias="mop-url")
    mop_comments: str = Field(..., alias="mop-comments")
    backout_duration: str = Field(..., alias="backout-duration")

class NetworkElement(BaseModel):
    ne_type: str = Field(..., alias="ne-type")
    ne_id: str = Field(..., alias="ne-id")

class ChangeRequestPayload(BaseModel):
    service_impact: str = Field(..., alias="service-impact")
    risk_level: str = Field(..., alias="risk-level")
    requester: str
    activity_category: str = Field(..., alias="activity-category")
    activity_type: str = Field(..., alias="activity-type")
    ticket_number: str = Field(..., alias="ticket-number")
    description: str
    network: str
    subnetwork: str
    location: Location
    scheduled_start_date_time: str = Field(..., alias="scheduled-start-date-time")
    scheduled_end_date_time: str = Field(..., alias="scheduled-end-date-time")
    outage_details: OutageDetails = Field(..., alias="outage-details")
    mop: List[MOP]
    submitter: str
    network_elements: List[NetworkElement] = Field(..., alias="network-elements")

# Output model for the response (adjust based on actual API response)
class ChangeRequestResponse(BaseModel):
    status: str
    request_id: Optional[str] = Field(None, alias="request-id")
    details: Optional[Dict[str, str]] = None

@app.post("/get_access_token", response_model=AccessTokenResponse)
async def get_access_token(request: AccessTokenRequest):
    TARGET_URL = "https://oa-uat.ebiz.verizon.com/oauth/client_credential/accesstoken?grant_type=client_credentials"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "client_id": request.client_id,
        "client_secret": request.client_secret
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(TARGET_URL, headers=headers, data=data)

        # Check if the external API returned an error
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        # Parse and return the response from the external API
        return response.json()

    except httpx.RequestError as e:
        # Handle connection issues
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")

@app.get("/get_user_access_token_info", response_model=UserAccessTokenInfoResponse)
async def get_user_access_token_info(username: str):
    BASE_URL = "https://oa-uat.ebiz.verizon.com"
    target_url = f"{BASE_URL}/msjv-kirke-changemanagement/userAccessTokenInfo?username={username}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(target_url)

        # Check if the external API returned an error
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        # Parse and return the response from the external API
        return response.json()

    except httpx.RequestError as e:
        # Handle connection issues
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    

@app.post("/create_change_request", response_model=ChangeRequestResponse)
async def create_change_request(
    payload: ChangeRequestPayload,
    authorization: str = Header(..., alias="Authorization"),
    jwt_token: str = Header(..., alias="jwtToken")
):
    CHANGE_REQUEST_URL = "https://oa-uat.ebiz.verizon.com/msjv-kirke-changemanagement/changerequests/v2"

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "Authorization": authorization,
        "jwtToken": jwt_token,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                CHANGE_REQUEST_URL, headers=headers, json=payload.dict(by_alias=True)
            )

        # Check if the external API returned an error
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        # Parse and return the response from the external API
        return response.json()

    except httpx.RequestError as e:
        # Handle connection issues
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")