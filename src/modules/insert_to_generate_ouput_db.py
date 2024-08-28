import os

from datetime import datetime
from tqdm.auto import tqdm

from src.database.crud import get_capture_history, get_generate_history, insert_database, check_capture_history_existed
from src.database.utils import create_generate_output
from src.database import models
from src.database.issues_database import engine
from src.modules.utils.capture_codegen import capture
from src.modules.utils.draw import draw_result
from src.config import configs


models.IssueBase.metadata.create_all(bind=engine)

start_date = datetime(2024, 8, 9)
end_date = datetime(2024, 8, 15)

page = 1
limit = 100
while True:
    rows = get_capture_history(start_date, end_date, page, limit)
    for capture_history in tqdm(rows):
        if check_capture_history_existed(capture_history.id):
            print(f"{capture_history.id} existed")
            continue
        capture_save_folder = os.path.join(configs['save_path'], str(capture_history.id))
        if not os.path.exists(capture_save_folder):
            os.makedirs(capture_save_folder)
        section_urls = capture_history.image_sections_capture
        section_atoms_urls = []
        section_codegen_urls = []
        generate_ids = []

        for i, section_url in tqdm(enumerate(section_urls)):
            generate_history = get_generate_history(section_url)
            if generate_history is None:
                section_atoms_urls.append("")
                section_codegen_urls.append("")
                generate_ids.append(0)
                continue
            generate_ids.append(generate_history.id)
            section_atoms_urls.append(generate_history.detected_url[0])
            output_builder = generate_history.output_builder
            save_codegen_path = os.path.join(capture_save_folder, str(i)+".png")
            try:
                capture(output_builder, save_codegen_path)
            except Exception as e:
                print(e)
                section_codegen_urls.append("")
                continue
            section_codegen_urls.append(save_codegen_path)

        draw_result(capture_history.image_source, capture_history.image_sections_capture, section_atoms_urls,\
                     section_codegen_urls, generate_ids, capture_history.page_url, capture_save_folder)
        row = create_generate_output(capture_history.id, capture_history.page_url, capture_history.image_source,\
                                    capture_history.image_sections_capture, section_atoms_urls, section_codegen_urls, generate_ids)
        try:
            insert_database(row)
        except Exception as e:
            print(e)
            continue

    if len(rows) < limit:
        break
    page += 1