from typing import Any, List

from pydantic import BaseModel, Field

class MOP(BaseModel):
    mop_url: str = Field(None, alias="mop-url")
    mop_comments: str = Field(None, alias="mop-comments")
    backout_duration: str = Field(None, alias="backout-duration")
    

class OutageInfo(BaseModel):
    number_of_outages: int = Field(None, alias="number-of-outages")
    outage_duration: int = Field(None, alias="outage-duration")
    outage_unit_of_measure: str = Field(None, alias="outage-unit-of-measure")
    

class OutageDetails(BaseModel):
    outage_info: OutageInfo = Field(None, alias="outage-info")

# Input model for the request payload
class Location(BaseModel):
    location_id: int= Field(None, alias="location-id")

class NetworkElement(BaseModel):
    ne_type: str = Field(None, alias="ne-type")
    ne_id: str = Field(None, alias="ne-id")
    
class CreateKirkeRequestPayload(BaseModel):

    service_impact: str = Field(None, alias="service-impact")
    risk_level: str = Field(None, alias="risk-level")
    requester: str = None
    activity_category: str = Field(None, alias="activity-category")
    activity_type: str = Field(None, alias="activity-type")
    ticket_number: str = Field(None, alias="ticket-number")
    description: str = None
    network: str = None
    subnetwork: str = None
    location: Location = None
    scheduled_start_date_time: str = Field(None, alias="scheduled-start-date-time")
    scheduled_end_date_time: str = Field(None, alias="scheduled-end-date-time")
    outage_details: OutageDetails = Field(None, alias="outage-details")
    mop: List[MOP] = None
    submitter: str = None
    network_elements: List[NetworkElement] = Field(None, alias="network-elements")
    





