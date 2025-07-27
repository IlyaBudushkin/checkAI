from docx import Document
from docx.shared import Inches

def filling_docx(template, new_text):
    doc = Document(template)

    # Проходим по всем параграфам и заменяем метки
    for paragraph in doc.paragraphs:
        if '{TEXT}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{TEXT}', new_text)

    doc.save('output.docx')