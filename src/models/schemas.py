## 
## Filename: Github-Project-AI-Agent/src/models/schemas.py
## Created Date: Thursday, April 30th 2026, 8:02:10 pm
## Author: Toa
## Description: Pydantic models for the Github Project AI Agent application, defining
##              the structure of tickets and project specifications.
##

from pydantic import BaseModel, Field
from typing import List, Literal

class Ticket(BaseModel):
    """
    Represents a single ticket/issue in the project.
    """
    title: str = Field(..., description="The title of the ticket")
    body: str = Field(..., description="The detailed description of the ticket")
    labels: List[str] = Field(default_factory=list, description="The labels for the ticket")
    effort: int | None = Field(default=None, description="The estimated effort for the ticket")
    priority: Literal["low", "medium", "high", "critical"] | None = Field(default=None, description="The priority of the ticket")
    epic: str | None = Field(default=None, description="The epic to which the ticket belongs")

class ProjectSpec(BaseModel):
    """
    Represents the specification for a project, including its structure and tickets.
    """
    project_name: str = Field(..., description="The name of the project")
    description: str = Field(..., description="A brief description of the project")
    columns: List[str] = Field(default=["Backlog", "Todo", "In Progress", "Review", "Done"], description="The columns in the project board")
    custom_fields: dict = Field(default={"effort": "number", "priority": "single select", "epic": "text"}, description="Custom fields for the project")
    tickets: List[Ticket] = Field(default_factory=list, description="The list of tickets in the project")
