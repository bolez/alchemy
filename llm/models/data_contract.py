
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

from llm.models.data_engineer import ColumnConstraint
from llm.models.data_governance import Owner, RetentionPolicy
from llm.models.data_steward import SLA
from llm.models.data_quality import ColumnValidationRule
from llm.models.data_engineer import DataRefresh


class ColumnSchema(BaseModel):
    column_name: str = Field(..., description="Name of the column in the data product")
    type: str = Field(..., description="Type of the column")
    constraints: Optional[List[ColumnConstraint]] = Field(None, description="Constraints for the column such as primary key, foreign key, unique, etc.")
    description: Optional[str] = Field(
        None, description="A meaningful description of the column's purpose or content don't change if it already mentioned in scheam"
    )
    pii: bool = Field(
        False, description="Flag indicating whether the column contains personally identifiable information (PII)"
    )


class DataContract(BaseModel):
    version: str
    model_name: str
    data_product_description: str
    tags: List[str]
    owner: Owner
    properties: List[ColumnSchema]
    rules: List[ColumnValidationRule]
    data_refresh: DataRefresh
    sla: SLA
    allowed_operations: List[str]
    retention_policy: RetentionPolicy
    contract_approved: bool
    approved_by: str