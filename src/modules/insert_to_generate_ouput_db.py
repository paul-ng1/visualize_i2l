import os
from tqdm import tqdm

from src.database.crud import get_capture_history, get_generate_history, insert_database
from src.database.utils import create_generate_output
from src.database import models
from src.database.issues_database import engine
from src.modules.utils.capture_codegen import capture
from src.config import configs


models.IssueBase.metadata.create_all(bind=engine)

captures_history = get_capture_history(100)

for capture_history in tqdm(captures_history):
    capture_save_folder = os.path.join(configs['save_path'], str(capture_history.id))
    if not os.path.exists(capture_save_folder):
        os.makedirs(capture_save_folder)
    section_urls = capture_history.image_sections_capture
    section_atoms_urls = []
    section_codegen_urls = []

    for i, section_url in tqdm(enumerate(section_urls)):
        generate_history = get_generate_history(section_url)
        if generate_history is None:
            section_atoms_urls.append("")
            section_codegen_urls.append("")
            continue
        import ipdb;ipdb.set_trace()
        section_atoms_urls.append(generate_history.detected_url[0])
        output_builder = generate_history.output_builder
        save_codegen_path = os.path.join(capture_save_folder, str(i)+".png")
        capture(output_builder, save_codegen_path)
        section_codegen_urls.append(save_codegen_path)

    row = create_generate_output(capture_history.id, capture_history.page_url, capture_history.image_source,\
                                 capture_history.image_sections_capture, section_atoms_urls, section_codegen_urls)
    insert_database(row)
