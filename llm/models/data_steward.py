from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class ColumnSemanticMetadata(BaseModel):
    """
    This class represents the semantic metadata for a column in a data product.
    It includes a description and a flag indicating whether the column contains personally identifiable information (PII).
    """
    column_name: str = Field(..., description="Name of the column in the data product")
    description: Optional[str] = Field(
        None, description="A meaningful description of the column's purpose or content don't change if it already mentioned in scheam"
    )
    pii: bool = Field(
        False, description="Flag indicating whether the column contains personally identifiable information (PII)"
    )


class IncidentResponse(BaseModel):
    """
    Defines the protocol for incident response when an SLA breach occurs.
    """
    notify: EmailStr = Field(..., description="Email address to be notified in the event of an SLA breach.")
    within_minutes: int = Field(..., description="The maximum time, in minutes, within which an incident must be responded to after it occurs.")


class SLA(BaseModel):
    """
    Specifies Service Level Agreements for data products, outlining expectations for data quality and delivery.
    """
    freshness: str = Field(..., description="The maximum permissible time lag between the data at the source and the data available to the consumer.")
    delivery_window: Optional[str] = Field(None, description="The expected timeframe during which data delivery is anticipated.")
    availability: Optional[str] = Field(None, description="The anticipated uptime or operational percentage of the system or data product.")
    max_null_rate: Optional[str] = Field(None, description="The highest acceptable percentage of null values allowed in critical columns.")
    incident_response: Optional[IncidentResponse] = Field(None, description="Details regarding the contact and expected response protocol when an SLA is violated.")


class SemanticMetadata(BaseModel):
    """
    This class represents the semantic metadata for a data product.
    It includes a description, tags, and column-level metadata.
    """
    data_product_description: str = Field(..., description="A meaningful description of the data product")
    tags: List[str] = Field(..., description="A list of appropriate tags for the data product")
    columns: List[ColumnSemanticMetadata] = Field(
        ..., description="List of column-level metadata including descriptions and PII flags"
    )
    sla: SLA = Field(..., description="Service Level Agreements for data products")
    