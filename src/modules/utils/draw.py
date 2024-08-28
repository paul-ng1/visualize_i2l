import os
import requests
from PIL import Image, ImageDraw, ImageFont


def draw_result(page_img_url, section_urls, section_atoms_urls, section_codegen_urls, generate_ids, page_url, save_folder):
    page = Image.open(requests.get(page_img_url, stream=True).raw)
    page_w, page_h = page.size[:2]

    padding_w = 200
    padding_h = 100
    padding_h_ = 100*(len(section_urls)-1)
    width = 4*page_w + 3*padding_w
    height = page_h + padding_h_
    img = Image.new('RGB', (width, height), color = (204,255,255))

    offset_page = (0, padding_h_//2)
    img.paste(page, offset_page)

    total_height = 0
    for i, section_url in enumerate(section_urls):
        section = Image.open(requests.get(section_url, stream=True).raw)
        section_w, section_h = section.size[:2]
        offset_section = (page_w+padding_w, total_height)
        img.paste(section, offset_section)

        offset_section_atoms = (2*(page_w+padding_w), total_height)
        offset_codegen = (3*(page_w+padding_w), total_height)
        offset_generate_id = (2*page_w+padding_w, total_height)
        if section_atoms_urls[i] != "":
            section_atoms = Image.open(requests.get(section_atoms_urls[i], stream=True).raw)
            if section_codegen_urls[i] != "":
                section_codegen = Image.open(section_codegen_urls[i])
                section_codegen = section_codegen.resize((section_w, section_h))
            else:
                section_codegen = Image.new('RGB', (section_w, section_h), color = (204,255,255))
        else:
            section_atoms = Image.new('RGB', (section_w, section_h), color = (204,255,255))
            section_codegen = Image.new('RGB', (section_w, section_h), color = (204,255,255))

        font = ImageFont.truetype("DejaVuSans.ttf", 50)
        I = ImageDraw.Draw(img)
        I.text(offset_generate_id, generate_ids[i],font=font, fill=(255,0,0))
        img.paste(section_atoms, offset_section_atoms)
        img.paste(section_codegen, offset_codegen)

        total_height += section_h+padding_h

    save_path = os.path.join(save_folder, "image.png")
    with open(save_path.replace('png', 'txt'), 'w') as f:
        f.write(page_url)
    
    img.save(save_path)
    
    