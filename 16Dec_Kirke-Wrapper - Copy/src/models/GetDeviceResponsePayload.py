from typing import List, Optional, Union
from pydantic import BaseModel, Field


class OccLocation(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    street: Optional[str] = None


class SiteCode(BaseModel):
    site_code_id: Optional[int] = Field(None, alias="site-code-id")
    name: Optional[str] = None


class Location(BaseModel):
    vz_loc_id: Optional[str] = Field(None, alias="vz-loc-id")
    vz_loc_name: Optional[str] = Field(None, alias="vz-loc-name")
    source_system: Optional[str] = Field(None, alias="source-system")
    clli: Optional[str] = None
    sensitive_clli: Optional[bool] = Field(None, alias="sensitive-clli")
    id: Optional[int] = None
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    site_codes: Optional[List[SiteCode]] = Field(None, alias="site-codes")
    timezone: Optional[str] = None
    timezone_id: Optional[str] = Field(None, alias="timezone-id")
    market_id: Optional[int] = Field(None, alias="market-id")
    market_name: Optional[str] = Field(None, alias="market-name")
    submarket_id: Optional[int] = Field(None, alias="submarket-id")
    submarket_name: Optional[str] = Field(None, alias="submarket-name")


class User(BaseModel):
    user_id: Optional[str] = Field(None, alias="user-id")
    display_name: Optional[str] = Field(None, alias="display-name")
    email: Optional[str] = None


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


class BackoutProcedureStep(BaseModel):
    step_seq: Optional[int] = Field(None, alias="step-seq")
    step_details: Optional[str] = Field(None, alias="step-details")


class NeApplication(BaseModel):
    application_name: Optional[str] = Field(None, alias="application-name")
    scope_of_impact: Optional[str] = Field(None, alias="scope-of-impact")
    market: Optional[str] = None
    sub_market: Optional[List[str]] = Field(None, alias="sub-market")


class NeAsp(BaseModel):
    asp_name: Optional[str] = Field(None, alias="asp-name")
    ne_application: Optional[List[NeApplication]] = Field(None, alias="ne-application")


class NeRegion(BaseModel):
    name: Optional[str] = None
    tenant_name: Optional[str] = Field(None, alias="tenant-name")


class NeApplicationContainer(BaseModel):
    name: Optional[str] = None
    ne_region: Optional[List[NeRegion]] = Field(None, alias="ne-region")


class ComputeNode(BaseModel):
    compute_node: Optional[List[str]] = Field(None, alias="compute-node")


class NeRegionVimCluster(BaseModel):
    name: Optional[str] = None
    compute_node: Optional[List[str]] = Field(None, alias="compute-node")


class NeSite(BaseModel):
    name: Optional[str] = None
    ne_region_vim_cluster: Optional[List[NeRegionVimCluster]] = Field(None, alias="ne-region-vim-cluster")


class NeVirtualElement(BaseModel):
    virtual_element_name: Optional[str] = Field(None, alias="virtual-element-name")


class Outage(BaseModel):
    outage_seq_id: Optional[int] = Field(None, alias="outage-seq-id")
    outage_start_time: Optional[str] = Field(None, alias="outage-start-time")
    outage_end_time: Optional[str] = Field(None, alias="outage-end-time")


class OutageContainer(BaseModel):
    outages: Optional[Outage] = None


class RequestNe(BaseModel):
    item_id: Optional[int] = Field(None, alias="item-id")
    item_status_id: Optional[int] = Field(None, alias="item-status-id")
    item_status_name: Optional[str] = Field(None, alias="item-status-name")
    implementation_status_id: Optional[int] = Field(None, alias="implementation-status-id")
    implementation_status_name: Optional[str] = Field(None, alias="implementation-status-name")
    actual_start_date_time: Optional[str] = Field(None, alias="actual-start-date-time")
    actual_end_date_time: Optional[str] = Field(None, alias="actual-end-date-time")
    ne_id: Optional[str] = Field(None, alias="ne-id")
    ne_type: Optional[str] = Field(None, alias="ne-type")
    ne_asp: Optional[List[NeAsp]] = Field(None, alias="ne-asp")
    ne_application: Optional[NeApplicationContainer] = Field(None, alias="ne-application")
    ne_site: Optional[NeSite] = Field(None, alias="ne-site")
    ne_virtual_element: Optional[List[NeVirtualElement]] = Field(None, alias="ne-virtual-element")
    number_of_outages: Optional[int] = Field(None, alias="number-of-outages")
    outage_duration: Optional[int] = Field(None, alias="outage-duration")
    outage_unit_of_measure: Optional[str] = Field(None, alias="outage-unit-of-measure")
    outages: Optional[List[OutageContainer]] = None


class RequestContact(BaseModel):
    vzid: Optional[str] = None
    contact_role_name: Optional[str] = Field(None, alias="contact-role-name")
    send_email: Optional[bool] = Field(None, alias="send-email")


class RequestConflict(BaseModel):
    freeze_name: Optional[str] = Field(None, alias="freeze-name")
    request_id: Optional[int] = Field(None, alias="request-id")
    conflict_rule_id: Optional[int] = Field(None, alias="conflict-rule-id")
    conflict_rule_name: Optional[str] = Field(None, alias="conflict-rule-name")


class RequestContent(BaseModel):
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
    carrier_name: Optional[str] = Field(None, alias="carrier-name")
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
    related_ticket: Optional[RelatedTicket] = Field(None, alias="related-ticket")
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
    backout_procedure: Optional[List[List[BackoutProcedureStep]]] = Field(None, alias="backout-procedure")
    request_ne_list: Optional[List[RequestNe]] = Field(None, alias="request-ne-list")
    request_contacts: Optional[List[RequestContact]] = Field(None, alias="request-contacts")
    request_conflicts: Optional[List[RequestConflict]] = Field(None, alias="request-conflicts")
    additional_prop1: Optional[dict] = Field(None, alias="additionalProp1")


class Pageable(BaseModel):
    sort: Optional[dict] = None
    page_number: Optional[int] = Field(None, alias="pageNumber")
    page_size: Optional[int] = Field(None, alias="pageSize")
    offset: Optional[int] = None
    paged: Optional[bool] = None
    unpaged: Optional[bool] = None


class Requests(BaseModel):
    content: Optional[List[RequestContent]] = None
    last: Optional[bool] = None
    pageable: Optional[Pageable] = None
    total_elements: Optional[int] = Field(None, alias="totalElements")
    total_pages: Optional[int] = Field(None, alias="totalPages")
    sort: Optional[dict] = None
    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = None
    size: Optional[int] = None
    number: Optional[int] = None
    empty: Optional[bool] = None



class GetDeviceResponsePayload(BaseModel):
    device_name: Optional[str] = Field(None, alias="deviceName")
    requests: Optional[Requests] = None
