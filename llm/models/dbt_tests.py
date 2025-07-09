from typing import List, Optional, Union, Literal, Dict, Any
from pydantic import BaseModel, Field, EmailStr


class DBTTest(BaseModel):
    column_name: str = Field(..., description="Name of the column to which the test applies")
    description: str = Field(
        ...,  description="Description of the column"
    )
    data_type: str = Field(
        ..., description="Data type of the column to which the test applies"
    )
    test_name: str = Field(..., description="Fully qualified name of the dbt test")
    test_parameters: Optional[Union[str, Dict[str, Any]]] = Field(
        None, description="Parameters specific to the dbt test. Can be a dict or a Jinja string."
    )

class AllColumnsTest(BaseModel):
    model_discription : str = Field(
        ...,
        description="Description of the model to which the tests apply"
    )
    model_name: str = Field(
        ...,
        description="Name of the model to which the tests apply"
    )
    tests: List[DBTTest] = Field(
        ...,
        description="List of dbt tests to be applied to all columns in the data product"
    )
