from pydantic import BaseModel, Field
from typing import List , Dict , Optional



class Employee(BaseModel):
    id: int
    name: str = Field(
        ...,
        min_length=3,
        max_length=10,
        description="Enter the name",
        example="Akshay Chavhan"
    )
    department: Optional[str] = "General"
    salary: float = Field(
        ...,
        ge=100000,
        le= 80000
    )

