import os
from docx import Document

def save_results_to_word(gpt_response, filename, output_folder="output_docs"):
    os.makedirs(output_folder, exist_ok=True)

    doc = Document()

    doc.add_paragraph(gpt_response if gpt_response else "Нет ответа от модели")

    full_path = os.path.join(output_folder, filename)
    doc.save(full_path)

