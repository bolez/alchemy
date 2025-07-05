from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class TableForeignKey(BaseModel):
    """
    This class represents a foreign key constraint for a table.
    It is used to define the foreign key relationship between two tables.
    """
    table: str = Field(..., description="Name of the table that contains the foreign key")
    column: str = Field(..., description="Name of the column that is the foreign key in the table")
    

class ColumnConstraint(BaseModel):
    primary_key: Optional[bool] = Field(False, description="Whether the column is a primary key or not") 
    unique: Optional[bool] = Field(False, description="Whether the column is unique or not")
    foreign_key_detailes: Optional[TableForeignKey] = Field(
        None, description="If foreign key is present, it should be a dictionary with 'table' and 'column'."
    )


class ColumnSchema(BaseModel):
    column_name: str = Field(..., description="Name of the column in the data product")
    type: str = Field(..., description="Type of the column")
    constraints: Optional[List[ColumnConstraint]] = Field(None, description="Constraints for the column such as primary key, foreign key, unique, etc.")


class DataRefresh(BaseModel):
    """
    Defines the data refresh characteristics for a data product.
    """
    frequency: Literal["hourly", "daily", "weekly", "monthly", "real-time"] = Field(..., description="How frequently the data product is refreshed.")
    refresh_method: Literal["full_load", "incremental", "streaming"] = Field(..., description="The method used to refresh the data, such as a complete reload, adding new changes, or continuous data flow.")
    schedule: Optional[str] = Field(None, description="A Cron expression (e.g., '0 0 * * *' for daily at midnight) specifying the exact schedule for data refreshes. Applicable for scheduled frequencies like hourly, daily, weekly, or monthly.")

class DataProductSchema(BaseModel):
    properties: List[ColumnSchema] = Field(
        ..., description="A list of dictionaries mapping column names to their `ColumnSchema` definitions"
    )
    data_refresh: Optional[DataRefresh] = Field(..., description="how frequentlly data refresh")
