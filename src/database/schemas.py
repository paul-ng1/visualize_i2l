from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class GenerateOutputBase(BaseModel):
    capture_history_id: int
    page_url: str
    capture_url: str
    sections_url: list[str]
    atoms_url: list[str] | None = None
    codegens_url: list[str] | None = None

    class Config:
        from_attributes = True


class GenerateOutputSchema(GenerateOutputBase):
    pass


class IssueTypeEnum(str, Enum):
    capture = 'capture'
    section = 'section'
    atoms = 'atoms'
    codegen = 'codegen'
    

class IssueBase(BaseModel):
    generate_output_id: int
    issue_image_url: str
    issue_type: IssueTypeEnum
    note: str | None = None
    checked: bool=False

    class Config:
        from_attributes = True


class IssueSchema(IssueBase):
    pass


