from src.database.schemas import GenerateOutputSchema
from src.database.models import GenerateOutput


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
