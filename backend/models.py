from typing import Optional
from datetime import datetime
from pydantic import BaseModel, AnyUrl


class VideoSchema(BaseModel):
    url: str
    construction_object: str
    date: str

    class Config:
        schema_extra = {
            "example": {
                "url": "filename",
                "construction_object": "Школа Архангельск",
                "date": "2022-06-01"
            }
        }