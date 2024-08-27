from src.database.schemas import GenerateOutputSchema, IssueSchema, IssueTypeEnum
from src.database.models import GenerateOutput, Issue


def create_generate_output(capture_history_id: int, page_url: str,\
                            capture_url: str, sections_url: list[str],\
                            atoms_url: str|None=None, codegens_url: str|None=None):
    row_schema = GenerateOutputSchema(
        capture_history_id=capture_history_id,
        page_url=page_url,
        capture_url=capture_url,
        sections_url=sections_url,
        atoms_url=atoms_url,
        codegens_url=codegens_url
    )
    row = GenerateOutput(**row_schema.model_dump())

    return row


def create_issue_row(generate_output_id: int, issue_image_url: str, issue_type: IssueTypeEnum, note: str|None=None, checked: bool=False):
    row_schema = IssueSchema(
        generate_output_id=generate_output_id,
        issue_image_url=issue_image_url,
        issue_type=issue_type,
        note=note,
        checked=checked
    )
    row = Issue(**row_schema.model_dump())

    return row
