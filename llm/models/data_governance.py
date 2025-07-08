from typing import List, Optional, Union, Literal
from pydantic import BaseModel, Field, EmailStr


class RetentionPolicy(BaseModel):
    """
    This class contains the retention policy for the data product.
    The retention policy is a dictionary where the keys are the retention policy types and the values are the retention policy details.
    type of retention policy such as 'time-based', 'soft-delete', 'hard-delete', 'archival'
    time-based: The data is retained for a specific period of time and then deleted.
    soft-delete: The data is marked as deleted but not actually deleted. The data can be restored later.
    hard-delete: The data is permanently deleted and cannot be restored.
    archival: The data is moved to an archive and can be restored later.
    rentention policy is important for
    Compliance: Meets legal and regulatory standards (e.g., GDPR, HIPAA, etc.)
    Privacy: Protects customer and sensitive data
    Cost Efficiency: Reduces storage costs by removing stale data
    Data Quality: Keeps datasets clean and relevant
    """
    type: Literal["time-based", "soft-delete", "hard-delete", "archival"] = Field(
        ...,
        description="Type of retention policy such as 'time-based', 'soft-delete', 'hard-delete', 'archival'"
    )
    duration: str = Field(
        ...,
        description="Duration of the retention policy such as '30 days', '1 year', '5 years', etc."
    )


class Owner(BaseModel):
    """
    Data product owner details
    This class contains the name and email of the data product owner.
    It is used to identify the person responsible for the data product.
    """
    name: str = Field(..., description="Name of the data product owner")
    email: EmailStr = Field(..., description="Email of the data product owner")


class DataGovernance(BaseModel):
    """
     - `owner` (team and email)
    - `retention_policy` (e.g., 90 days, 1 year, 7 years; time-based/soft-delete)
    - `allowed_operations` (read/write/update/delete)
    - `sensitive_data` (confirm which fields are PII or restricted)
    - `contract_approved` and `approved_by`

    """
    owner: Owner = Field(..., description="Data product Owner details")
    allowed_operations: List[Literal["read", "write", "update", "delete"]] = Field(
            ['read'],
            description="Allowed operations on the data product such as 'read', 'write', 'update', 'delete'"
        )
    contract_approved: bool = Field(
            ...,
            description="Whether the data contract is approved or not"
        )
    approved_by: Optional[EmailStr] | None = Field(
            None, 
            description="Email of the person who approved the data contract"
        )
    retention_policy: RetentionPolicy = Field(
            ..., 
            description="Retention policy for the data product, and more details use `RetentionPolicy` class"
        )
