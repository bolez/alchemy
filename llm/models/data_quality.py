from typing import List, Optional, Union, Literal
from pydantic import BaseModel, Field
from llm.utils.data_quality_rules import all_rules

class SchemaColunDataQuality(BaseModel):
    """
    This class represents the data quality checks for a schema.
    It includes checks for null values, uniqueness, and range constraints.
    It is used to ensure the quality of the data in the schema.
    """
    column_name: str = Field(..., description="Name of the column in the data product")
    enum: Optional[List[str]] = Field(None, description="Allowed values for categorical columns")
    minimum: Optional[float] = Field(None, description="Minimum value for numeric columns")
    maximum: Optional[float] = Field(None, description="Maximum value for numeric columns")


class DataQualityRule(BaseModel):
    """
    This class contains the validation rules for the data product.
    The validation rules are a dictionary where the keys are the validation rule types and the values are the validation rule details.
    Used to define constraints or checks that must be applied to the data at runtime or ingestion time to ensure data quality, accuracy, and consistency. 
    These rules help prevent bad or unexpected data from entering your system.
    Types of validation rules include:
    enum:	Ensures values are from a defined set (e.g., statuses like shipped, cancelled)
    range: 	Numeric or date fields must fall within a range
    regex:	Text fields must match a regular expression pattern
    not_null:	Column must not contain null values
    unique:	Values in a column must be unique
    foreign_key:	Value must exist in another referenced table
    custom:	Any other custom validation logic, such as checking for specific formats, patterns, or business rules
    Examples include: email format, phone number format, date format, etc.
    etc.
    """
    name: str = Field(..., description="Name of the validation rule")
    type: Literal[*all_rules] = Field(..., description="Type of the validation rule")
    allowed_values: Optional[List[Union[str, int]]] = Field(None, description="Allowed values for enum-type rules")
    min: Optional[float] = Field(None, description="Minimum value for range-type rules")
    max: Optional[float] = Field(None, description="Maximum value for range-type rules")
    pattern: Optional[str] = Field(None, description="Regex pattern for regex-type rules or any specific pattern")
    enum: Optional[List[str]] = Field(None, description="Ensures values are from a defined set (e.g., statuses like shipped, cancelled)")
    logic: Optional[str] = Field(None, description="Any other custom validation logic, such as checking for specific formats, patterns, or business rules")

class ColumnValidationRule(BaseModel):
    """
    A list of validation rules applied to a specific column.
    """
    column: str = Field(..., description="Target column name")
    column_rules: List[DataQualityRule]

class ValidationRule(BaseModel):
    """
    The top-level schema capturing validation rules across all columns of a model/table.
    """
    model_name: str
    rules: List[ColumnValidationRule]

