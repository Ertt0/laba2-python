from datetime import UTC, datetime
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, StringConstraints, field_validator


class Level(Enum): # набор именованных допустмимых значений(закрытый список вариантов у поля)
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class Event(BaseModel):
    timestamp: datetime
    level: Level
    source: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    message: str
   
    @field_validator("timestamp")
    @classmethod 
    def utc(cls, value):
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value