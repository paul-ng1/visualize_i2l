import os
from tqdm import tqdm

from read_db import DatabaseConnection , get_capture_history, get_generate_history
from draw import draw_result
from capture_codegen import capture


ssh_host = '3.93.68.57'
ssh_port = 22
ssh_user = 'ec2-user'
ssh_private_key = '~/Downloads/gem-x-prod-system-admin.pem'

db_host = 'image2layout-detection.chm9jqqz3liy.us-east-1.rds.amazonaws.com'  # Replace with your EC2 instance's public DNS
db_port = 5432
db_name = ''  # Replace with your database name
db_user = 'postgres'  # Replace with your database username
db_password = 'Uxc6AyhAWe6nHsmv'  # Replace with your database password

save_foler = "result"

db_connection = DatabaseConnection(ssh_host, ssh_port, ssh_user, ssh_private_key, db_host, db_port, db_name, db_user, db_password)
captures_history = get_capture_history(db_connection, 5)

for capture_history in tqdm(captures_history):
    capture_save_folder = os.path.join(save_foler, str(capture_history[0]))
    if not os.path.exists(capture_save_folder):
        os.makedirs(capture_save_folder)
    section_urls = capture_history[2]
    section_atoms_urls = []
    section_codegen_urls = []

    for i, section_url in enumerate(section_urls):
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

