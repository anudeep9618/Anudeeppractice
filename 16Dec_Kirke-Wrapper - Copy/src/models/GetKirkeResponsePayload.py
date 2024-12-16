from typing import Optional, Any, List, Dict

from pydantic import BaseModel, Field, RootModel

class OccLocation(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    street: Optional[str] = None

# Define RequestConflict model
class RequestConflict(BaseModel):
    request_id: int = Field(alias="request-id")
    conflict_rule_id: int = Field(alias="conflict-rule-id")
    conflict_rule_name: str = Field(alias="conflict-rule-name")
    freeze_name: Optional[str] = Field(alias="freeze-name")

# Define RelatedTicket model
class RelatedTicket(BaseModel):
    ticket_source_id: Optional[int] = Field(None, alias="ticket-source-id")
    ticket_source_name: Optional[str] = Field(None, alias="ticket-source-name")
    ticket_number: Optional[str] = Field(None, alias="ticket-number")
                                         
class MopFile(BaseModel):
    file_name: Optional[str] = Field(None, alias="file-name")
    file_path: Optional[str] = Field(None, alias="file-path")

class MopStep(BaseModel):
    step_seq: Optional[int] = Field(None, alias="step-seq")
    step_details: Optional[str] = Field(None, alias="step-details")

# Define User model
class User(BaseModel):
    user_id: Optional[str] = Field(None, alias="user-id")
    display_name: Optional[str] = Field(None, alias="display-name")
    email: Optional[str] = None

class RequestNE(BaseModel):
    item_id: Optional[int] = Field(None, alias="item-id")
    item_status_id: Optional[int] = Field(None, alias="item-status-id")
    item_status_name: Optional[str] = Field(None, alias="item-status-name")
    implementation_status_id: Optional[int] = Field(None, alias="implementation-status-id")
    implementation_status_name: Optional[str] = Field(None, alias="implementation-status-name")
    actual_start_date_time: Optional[str] = Field(None, alias="actual-start-date-time")
    actual_end_date_time: Optional[str] = Field(None, alias="actual-end-date-time")
    ne_id: Optional[str] = Field(None, alias="ne-id")
    ne_type: Optional[str] = Field(None, alias="ne-type")
    ne_asp: Optional[List[dict]] = None  # Placeholder for nested 'ne-asp' list
    ne_application: Optional[dict] = None  # Placeholder for 'ne-application' dictionary
    ne_site: Optional[dict] = None  # Placeholder for 'ne-site' dictionary
    ne_virtual_element: Optional[List[dict]] = None  # Placeholder for 'ne-virtual-element' list
    number_of_outages: Optional[int] = Field(None, alias="number-of-outages")
    outage_duration: Optional[int] = Field(None, alias="outage-duration")
    outage_unit_of_measure: Optional[str] = Field(None, alias="outage-unit-of-measure")
    outages: Optional[List[dict]] = None  # Placeholder for 'outages' list

# Define Location model
class Location(BaseModel):
    vz_loc_id: Optional[str] = Field(None, alias="vz-loc-id")
    vz_loc_name: Optional[str] = Field(None, alias="vz-loc-name")
    source_system: Optional[str] = Field(None, alias="source-system")
    source_system_site_id: Optional[str] = Field(None, alias="source-system-site-id")
    clli: Optional[str] = None
    sensitive_clli: Optional[bool] = Field(None, alias="sensitive-clli")
    id: Optional[int] = None
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    site_codes: Optional[List[dict]] = Field(None, alias="site-codes")
    timezone: Optional[str] = None
    timezone_id: Optional[str] = Field(None, alias="timezone-id")
    market_id: Optional[int] = Field(None, alias="market-id")
    market_name: Optional[str] = Field(None, alias="market-name")
    submarket_id: Optional[int] = Field(None, alias="submarket-id")
    submarket_name: Optional[str] = Field(None, alias="submarket-name")
	
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

class ChangeRequestResponseItem(BaseModel):
    request_id: Optional[int] = Field(None, alias="request-id")
    plan_id: Optional[int] = Field(None, alias="plan-id")
    request_status: Optional[str] = Field(None, alias="request-status")
    approval_comments: Optional[str] = Field(None, alias="approval-comments")
    scheduled_start_date_time: Optional[str] = Field(None, alias="scheduled-start-date-time")
    scheduled_end_date_time: Optional[str] = Field(None, alias="scheduled-end-date-time")
    network_id: Optional[int] = Field(None, alias="network-id")
    network_name: Optional[str] = Field(None, alias="network-name")
    lead_time_violated: Optional[bool] = Field(None, alias="lead-time-violated")
    maintenance_window_violated: Optional[bool] = Field(None, alias="maintenance-window-violated")
    subnetwork_id: Optional[int] = Field(None, alias="subnetwork-id")
    subnetwork_name: Optional[str] = Field(None, alias="subnetwork-name")
    individual_cell_site: Optional[bool] = Field(None, alias="individual-cell-site")
    mpe_id: Optional[int] = Field(None, alias="mpe-id")
    change_type_id: Optional[int] = Field(None, alias="change-type-id")
    change_type_name: Optional[str] = Field(None, alias="change-type-name")
    occ_location: Optional[OccLocation] = Field(None, alias="occ-location")
    carrier_name: Optional[str] = None
    impact_level_id: Optional[int] = Field(None, alias="impact-level-id")
    impact_level_name: Optional[str] = Field(None, alias="impact-level-name")
    service_impact_id: Optional[int] = Field(None, alias="service-impact-id")
    service_impact_name: Optional[str] = Field(None, alias="service-impact-name")
    risk_level_id: Optional[int] = Field(None, alias="risk-level-id")
    risk_level_name: Optional[str] = Field(None, alias="risk-level-name")
    activity_category_id: Optional[int] = Field(None, alias="activity-category-id")
    activity_category_name: Optional[str] = Field(None, alias="activity-category-name")
    activity_type_id: Optional[int] = Field(None, alias="activity-type-id")
    activity_type_name: Optional[str] = Field(None, alias="activity-type-name")
    description: Optional[str] = None
    location: Optional[Location] = None
    requester: Optional[User] = None
    submitter: Optional[User] = None
    implementer: Optional[User] = None
    related_ticket: Optional[RelatedTicket] = None
    reference_id: Optional[str] = Field(None, alias="reference-id")
    project_id: Optional[int] = Field(None, alias="project-id")
    created_date_time: Optional[str] = Field(None, alias="created-date-time")
    last_modified_by: Optional[User] = Field(None, alias="last-modified-by")
    last_modified_date_time: Optional[str] = Field(None, alias="last-modified-date-time")
    mop_files: Optional[List[MopFile]] = Field(None, alias="mop-files")
    mop_url: Optional[str] = Field(None, alias="mop-url")
    mop_id: Optional[str] = Field(None, alias="mop-id")
    mop_steps: Optional[List[MopStep]] = Field(None, alias="mop-steps")
    mop_comments: Optional[str] = Field(None, alias="mop-comments")
    backout_duration: Optional[str] = Field(None, alias="backout-duration")
    backout_procedure: Optional[List[List[MopStep]]] = Field(None, alias="backout-procedure")
    request_ne_list: Optional[List[RequestNE]] = Field(None, alias="request-ne-list")
    request_contacts: Optional[List[dict]] = Field(None, alias="request-contacts")
    request_conflicts: Optional[List[dict]] = Field(None, alias="request-conflicts")
    additionalProp1: Optional[Dict] = None

class GetKirkeResponsePayload(RootModel):
    root: List[ChangeRequestResponseItem]





