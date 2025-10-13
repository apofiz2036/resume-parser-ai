import os
from docx import Document

def save_results_to_word(candidate, output_folder="output_docs", filename=None):
    os.makedirs(output_folder, exist_ok=True)

    doc = Document()

    for key, value in candidate.items():
        doc.add_heading(key.capitalize(), level=2)

        if value is None:
            doc.add_paragraph("Нет данных")
        elif isinstance(value, dict):
            for k, v in value.items():
                doc.add_paragraph(f"{k}: {v}")
        elif isinstance(value, str):
            if len(value) > 500:
                sentences = value.split('. ')
                for sentence in sentences:
                    if sentence.strip():
                        doc.add_paragraph(sentence.strip() + '.')
            else:
                doc.add_paragraph(value)
        else:
            doc.add_paragraph(str(value))

    if filename is None:
        filename = f"candidate_{hash(str(candidate))}.docx"

    full_path = os.path.join(output_folder, filename)
    doc.save(full_path)
    print(f"Сохранено: {full_path}")

