from typing import List, Optional
from pydantic import BaseModel, Field

# Define the nested models as needed
class Pageable(BaseModel):
    page_number: Optional[int] = Field(None, alias="pageNumber")
    page_size: Optional[int] = Field(None, alias="pageSize")
    sort: Optional[dict] = None
    offset: Optional[int]
    unpaged: Optional[bool]
    paged: Optional[bool]

class Sort(BaseModel):
    empty: Optional[bool]
    sorted: Optional[bool]
    unsorted: Optional[bool]

class RequestContent(BaseModel):
    # Define all fields of RequestContent here
    pass

class Requests(BaseModel):
    content: Optional[List[RequestContent]] = Field(None, alias="content")
    last: Optional[bool] = Field(None, alias="last")
    pageable: Optional[Pageable] = Field(None, alias="pageable")
    total_elements: Optional[int] = Field(None, alias="totalElements")
    total_pages: Optional[int] = Field(None, alias="totalPages")
    sort: Optional[Sort] = Field(None, alias="sort")
    number_of_elements: Optional[int] = Field(None, alias="numberOfElements")
    first: Optional[bool] = Field(None, alias="first")
    size: Optional[int] = Field(None, alias="size")
    number: Optional[int] = Field(None, alias="number")
    empty: Optional[bool] = Field(None, alias="empty")

class GetDeviceResponsePayload(BaseModel):
    device_name: Optional[str] = Field(None, alias="deviceName")
    requests: Optional[Requests] = Field(None, alias="requests")