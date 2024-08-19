import os
from tqdm import tqdm

from read_db import DatabaseConnection , get_capture_history, get_generate_history
from draw import draw_result
from capture_codegen import capture
from utils import load_config

configs = load_config()

db_connection = DatabaseConnection(configs['ssh']['host'],
                                   configs['ssh']['port'],
                                   configs['ssh']['user'],
                                   configs['ssh']['private_key'],
                                   configs['db']['host'],
                                   configs['db']['port'],
                                   configs['db']['name'],
                                   configs['db']['user'],
                                   configs['db']['password'],
)

captures_history = get_capture_history(db_connection, 100)

for capture_history in tqdm(captures_history):
    capture_save_folder = os.path.join(configs['save_path'], str(capture_history[0]))
    if not os.path.exists(capture_save_folder):
        os.makedirs(capture_save_folder)
    section_urls = capture_history[2]
    section_atoms_urls = []
    section_codegen_urls = []

    for i, section_url in tqdm(enumerate(section_urls)):
        generate_history = get_generate_history(db_connection, section_url)
        if generate_history is None:
            section_atoms_urls.append("")
            section_codegen_urls.append("")
            continue
        section_atoms_urls.append(generate_history[6][0])
        output_builder = generate_history[3]
        save_codegen_path = os.path.join(capture_save_folder, str(i)+".png")
        capture(output_builder, save_codegen_path)
        section_codegen_urls.append(save_codegen_path)

    draw_result(capture_history[1], section_urls, section_atoms_urls, section_codegen_urls, capture_history[5], capture_save_folder)

