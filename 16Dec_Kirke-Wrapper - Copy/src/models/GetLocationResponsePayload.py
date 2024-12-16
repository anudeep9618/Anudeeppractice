from typing import List
from models.CreateKirkeResponsePayload import Location
from pydantic import BaseModel, Field, RootModel


class GetLocationResponsePayload(BaseModel):
    locations: List[Location]