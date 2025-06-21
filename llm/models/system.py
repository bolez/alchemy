from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
import json


class UserRequest(BaseModel):
    schema_file_path: str = Field(
        ...,
        description="Path to the schema file that contains the data product schema in YAML format"
    )
    initial_user_details: Optional[Dict[str, Any]] = Field(
        ...,
        description="Initial user details and context extracted from the user's request"
    )
    source_schemas: Optional[Dict[str, Any]] = Field(
        ...,
        description="Source schemas extracted from the schema file"
    )

    errors: Optional[List[str]] = Field(
        [],
        description="List of errors encountered during the data contract creation process"
    )
    agent_finished: Optional[bool] = Field(
        False,
        description="Whether the data contract creation process is finished or not"
    )

    @field_validator("initial_user_details", mode="before")
    def parse_initial_user_details(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                raise ValueError("initial_user_details must be a valid dictionary or JSON string")
        return v

    @field_validator("source_schemas", mode="before")
    def parse_source_schemas(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                raise ValueError("""source_schemas must be a valid dictionary or JSON string""")
        return v
    