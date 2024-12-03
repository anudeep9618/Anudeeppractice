from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, RootModel, Field
from typing import List, Optional, Dict, Any
import httpx

app = FastAPI()

class AccessTokenRequest(BaseModel):
    client_id: str
    client_secret: str

class AccessTokenResponse(BaseModel):
    refresh_token_expires_in: str
    api_product_list: str
    api_product_list_json: List[str]
    organization_name: str
    token_type: str
    issued_at: str
    client_id: str
    access_token: str
    application_name: str
    scope: str
    expires_in: str
    refresh_count: str
    status: str


# class UserAccessTokenInfoRequest(BaseModel):
#     username: str

class UserAccessTokenInfoResponse(BaseModel):
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

from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class OCCLocation(BaseModel):
    city: str
    state: str
    country: str
    street: str

class SiteCode(BaseModel):
    site_code_id: int
    name: str

class Location(BaseModel):
    vz_loc_id: str
    vz_loc_name: str
    source_system: str
    clli: str
    sensitive_clli: bool
    id: int
    name: str
    address: str
    city: str
    state: str
    country: str
    site_codes: List[SiteCode]
    timezone: str
    timezone_id: str
    market_id: int
    market_name: str
    submarket_id: int
    submarket_name: str

class User(BaseModel):
    user_id: str
    display_name: str
    email: str

class RelatedTicket(BaseModel):
    ticket_source_id: int
    ticket_source_name: str
    ticket_number: str

class MopFile(BaseModel):
    file_name: str
    file_path: str

class MopStep(BaseModel):
    step_seq: int
    step_details: str

class BackoutStep(BaseModel):
    step_seq: int
    step_details: str

class NEApplication(BaseModel):
    application_name: str
    scope_of_impact: str
    market: str
    sub_market: List[str]

class NERegion(BaseModel):
    name: str
    tenant_name: str

class NECluster(BaseModel):
    name: str
    compute_node: List[str]

class NEVirtualElement(BaseModel):
    virtual_element_name: str

class NEOutage(BaseModel):
    outage_seq_id: int
    outage_start_time: str
    outage_end_time: str

class RequestNE(BaseModel):
    item_id: int
    item_status_id: int
    item_status_name: str
    implementation_status_id: int
    implementation_status_name: str
    actual_start_date_time: str
    actual_end_date_time: str
    ne_id: str
    ne_type: str
    ne_asp: Optional[List[Dict[str, Any]]]
    ne_application: Optional[Dict[str, Any]]
    ne_site: Optional[Dict[str, Any]]
    ne_virtual_element: Optional[List[NEVirtualElement]]
    number_of_outages: int
    outage_duration: int
    outage_unit_of_measure: str
    outages: Optional[List[Dict[str, NEOutage]]]

class RequestContact(BaseModel):
    vzid: str
    contact_role_name: str
    send_email: bool

class RequestConflict(BaseModel):
    freeze_name: str
    request_id: int
    conflict_rule_id: int
    conflict_rule_name: str

class ChangeRequestResponseItem(BaseModel):
    request_id: int
    plan_id: int
    request_status: str
    approval_comments: Optional[str]
    scheduled_start_date_time: str
    scheduled_end_date_time: str
    network_id: int
    network_name: str
    lead_time_violated: bool
    maintenance_window_violated: bool
    subnetwork_id: int
    subnetwork_name: str
    individual_cell_site: bool
    mpe_id: int
    change_type_id: int
    change_type_name: str
    occ_location: OCCLocation
    carrier_name: str
    impact_level_id: int
    impact_level_name: str
    service_impact_id: int
    service_impact_name: str
    risk_level_id: int
    risk_level_name: str
    activity_category_id: int
    activity_category_name: str
    activity_type_id: int
    activity_type_name: str
    description: str
    location: Location
    requester: User
    submitter: User
    implementer: User
    related_ticket: Optional[RelatedTicket]
    reference_id: str
    project_id: int
    created_date_time: str
    last_modified_by: User
    last_modified_date_time: str
    mop_files: Optional[List[MopFile]]
    mop_url: Optional[str]
    mop_id: Optional[str]
    mop_steps: Optional[List[MopStep]]
    mop_comments: Optional[str]
    backout_duration: str
    backout_procedure: Optional[List[List[BackoutStep]]]
    request_ne_list: Optional[List[RequestNE]]
    request_contacts: Optional[List[RequestContact]]
    request_conflicts: Optional[List[RequestConflict]]
    additional_prop1: Optional[Dict[str, Any]]

class ChangeRequestResponse(RootModel):
    root: List[List[ChangeRequestResponseItem]]

class GetChangeRequestResponse(RootModel):
    root: List[ChangeRequestResponseItem]

class AccessMethodResponse(BaseModel):
    token: str

@app.post("/get_access_token_method", response_model=AccessMethodResponse)
async def get_access_token_method(request: AccessTokenRequest):
    # Replace hardcoded credentials with environment variables or config variables
    VALID_CLIENT_ID = "svc-vsop-sa"
    VALID_CLIENT_SECRET = "sdfdsgsdadsgeaga"

    # Validate credentials
    if request.client_id != VALID_CLIENT_ID or request.client_secret != VALID_CLIENT_SECRET:
        raise HTTPException(status_code=400, detail="Incorrect Client ID or Client Password")

    # Generate token (use a secure approach in production)
    token = "123456789opoiuyttt"

    return AccessMethodResponse(token=token)

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
        
        # Parse and validate response
        try:
            response_data = response.json()
            return AccessTokenResponse.model_validate(response_data)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Response validation failed: {str(e)}"
            )

        # return response.json()

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
        
       # Parse and validate response
        try:
            response_data = response.json()
            return UserAccessTokenInfoResponse.model_validate(response_data)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Response validation failed: {str(e)}"
            )
        # Parse and return the response from the external API
        # return response.json()

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
                CHANGE_REQUEST_URL, headers=headers, json=payload.model_dump(by_alias=True)
            )

        # Check if the external API returned an error
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
       # Parse and validate response
        try:
            response_data = response.json()
            return ChangeRequestResponse.model_validate(response_data)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Response validation failed: {str(e)}"
            )
        
        # Parse and return the response from the external API
        # return response.json()

    except httpx.RequestError as e:
        # Handle connection issues
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    
@app.get("/get_change_request", response_model=GetChangeRequestResponse)
async def get_change_request(
    request_id: int,
    authorization: str = Header(..., alias="Authorization"),
    jwt_token: str = Header(..., alias="jwtToken")
):
    """
    Fetch details for a specific change request by ID.
    
    Args:
        request_id: The ID of the change request to retrieve.
        authorization: Bearer token for authorization.
        jwt_token: JWT token for additional validation.

    Returns:
        The details of the change request.
    """
    BASE_URL = "https://oa-uat.ebiz.verizon.com"
    target_url = f"{BASE_URL}/msjv-kirke-changemanagement/changerequests/{request_id}"

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "Authorization": authorization,
        "jwtToken": jwt_token,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(target_url, headers=headers)

        # Check for HTTP errors
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        # Parse and validate response
        try:
            response_data = response.json()
            return GetChangeRequestResponse(**response_data)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Response validation failed: {str(e)}"
            )

    except httpx.RequestError as e:
        # Handle connection issues
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")