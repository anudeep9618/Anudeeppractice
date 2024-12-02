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

# Define Location model
class Location(BaseModel):
    vz_loc_id: str = Field(alias="vz-loc-id")
    vz_loc_name: str = Field(alias="vz-loc-name")
    clli: str
    sensitive_clli: bool = Field(alias="sensitive-clli")
    id: int
    name: Optional[str]
    address: str
    city: str
    state: str
    country: str
    timezone: str
    timezone_id: str = Field(alias="timezone-id")
    market_id: Optional[Any] = Field(alias="market-id")
    market_name: Optional[Any] = Field(alias="market-name")
    submarket_id: Optional[Any] = Field(alias="submarket-id")
    submarket_name: Optional[Any] = Field(alias="submarket-name")
    source_system_site_id: str = Field(alias="source-system-site-id")
    source_system: str = Field(alias="source-system")

# Define User model
class User(BaseModel):
    user_id: str = Field(alias="user-id")
    display_name: str = Field(alias="display-name")
    email: str

# Define RelatedTicket model
class RelatedTicket(BaseModel):
    ticket_source_id: Optional[Any] = Field(alias="ticket-source-id")
    ticket_source_name: Optional[Any] = Field(alias="ticket-source-name")
    ticket_number: Optional[Any]

# Define RequestNeListItem model
class RequestNeListItem(BaseModel):
    item_id: int = Field(alias="item-id")
    item_name: str = Field(alias="item-name")
    item_status_id: int = Field(alias="item-status-id")
    item_status_name: str = Field(alias="item-status-name")
    implementation_status_id: Optional[int] = Field(alias="implementation-status-id")
    implementation_status_name: Optional[str] = Field(alias="implementation-status-name")
    actual_start_date_time: str = Field(alias="actual-start-date-time")
    actual_end_date_time: str = Field(alias="actual-end-date-time")
    outages: List[Dict[str, Optional[Any]]]
    ne_type: str = Field(alias="ne-type")
    is_ne_inventoried: bool = Field(alias="is-ne-inventoried")
    ne_id: str = Field(alias="ne-id")

# Define RequestConflict model
class RequestConflict(BaseModel):
    request_id: int = Field(alias="request-id")
    conflict_rule_id: int = Field(alias="conflict-rule-id")
    conflict_rule_name: str = Field(alias="conflict-rule-name")
    freeze_name: Optional[str] = Field(alias="freeze-name")

# Define main ChangeRequestResponseItem model
class ChangeRequestResponseItem(BaseModel):
    request_id: int = Field(alias="request-id")
    plan_id: int = Field(alias="plan-id")
    request_status: str = Field(alias="request-status")
    approval_comments: Optional[Any] = Field(alias="approval-comments")
    scheduled_start_date_time: str = Field(alias="scheduled-start-date-time")
    scheduled_end_date_time: str = Field(alias="scheduled-end-date-time")
    network_id: int = Field(alias="network-id")
    network_name: str = Field(alias="network-name")
    subnetwork_id: int = Field(alias="subnetwork-id")
    subnetwork_name: str = Field(alias="subnetwork-name")
    change_type_id: int = Field(alias="change-type-id")
    change_type_name: str = Field(alias="change-type-name")
    impact_level_id: int = Field(alias="impact-level-id")
    impact_level_name: str = Field(alias="impact-level-name")
    activity_category_id: int = Field(alias="activity-category-id")
    activity_category_name: str = Field(alias="activity-category-name")
    activity_type_id: int = Field(alias="activity-type-id")
    activity_type_name: str = Field(alias="activity-type-name")
    individual_cell_site: bool = Field(alias="individual-cell-site")
    service_impact_id: int = Field(alias="service-impact-id")
    service_impact_name: str = Field(alias="service-impact-name")
    risk_level_id: int = Field(alias="risk-level-id")
    risk_level_name: str = Field(alias="risk-level-name")
    description: str
    location: Location
    occ_location: Optional[Any] = Field(alias="occ-location")
    carrier_name: Optional[Any] = Field(alias="carrier-name")
    requester: User
    submitter: User
    implementer: Optional[Any]
    related_ticket: RelatedTicket
    reference_id: Optional[Any] = Field(alias="reference-id")
    project_id: Optional[Any] = Field(alias="project-id")
    mpe_id: Optional[Any] = Field(alias="mpe-id")
    lead_time_violated: bool = Field(alias="lead-time-violated")
    maintenance_window_violated: bool = Field(alias="maintenance-window-violated")
    created_date_time: str = Field(alias="created-date-time")
    last_modified_by: Optional[Any] = Field(alias="last-modified-by")
    last_modified_date_time: str = Field(alias="last-modified-date-time")
    mop_files: List[Any] = Field(alias="mop-files")
    mop_url: str = Field(alias="mop-url")
    mop_id: Optional[Any] = Field(alias="mop-id")
    mop_steps: List[Any] = Field(alias="mop-steps")
    mop_comments: str = Field(alias="mop-comments")
    backout_duration: str = Field(alias="backout-duration")
    backout_procedure: List[Any] = Field(alias="backout-procedure")
    request_ne_list: List[RequestNeListItem] = Field(alias="request-ne-list")
    request_contacts: List[Any] = Field(alias="request-contacts")
    request_conflicts: List[RequestConflict] = Field(alias="request-conflicts", default_factory=list)
    nen_services: Optional[Any] = Field(alias="nen-services")
    policy_justification: List[Any] = Field(alias="policy-justification")

class ChangeRequestResponse(RootModel):
    root: List[List[ChangeRequestResponseItem]]

class GetChangeRequestResponse(RootModel):
    root: List[ChangeRequestResponseItem]

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