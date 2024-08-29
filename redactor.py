import fitz
import re
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

# Função que retorna os padrões de regex padrão
def get_default_patterns():
    return {
        "agravante": re.compile(r'^(?!.*\b(?:PARTES|ADVOGADOS)\b)([A-ZÀ-ÖØ-öø-ÿ\s]{2,})\s*\(AGRAVANTE\)', re.IGNORECASE | re.MULTILINE),
        "agravado": re.compile(r'^(?!.*\b(?:PARTES|ADVOGADOS)\b)([A-ZÀ-ÖØ-öø-ÿ\s]{2,})\s*\(AGRAVADO\)', re.IGNORECASE | re.MULTILINE),
        "advogado": re.compile(r'^(?!.*\b(?:PARTES|ADVOGADOS)\b)([A-ZÀ-ÖØ-öø-ÿ\s]{2,})\s*\(ADVOGADO\)', re.IGNORECASE | re.MULTILINE),
        "cpf": re.compile(r'\d{3}\s?\.\s?\d{3}\s?\.\s?\d{3}\s?-\s?\d{2}'),
        "rg": re.compile(r'\d{2}\s?\.\s?\d{3}\s?\.\s?\d{3}\s?-\s?\d{1}'),
        "phone": re.compile(r'\(?\d{2}\)?\s?\d{4,5}\s?-\s?\d{4}'),
        "email": re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
        "process_number": re.compile(r'\d{7}\s?-\s?\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}'),
        "credit_card": re.compile(r'\b(?:\d\s?[ -]*?\s?){13,16}\b'),
        "cnh": re.compile(r'\b\d{11}\b'),
        "oab": re.compile(r'OAB\s?\/\s?[A-Z]{2}\s?\d{1,6}'),
        "old_plate": re.compile(r'[A-Z]{3}\s?-\s?\d{4}'),  # Exemplo: ABC-1234
        "new_plate": re.compile(r'[A-Z]{3}\s?\d\s?[A-Z]\s?\d{2}'),  # Exemplo: ABC1D23
        "address": re.compile(
            r'\b(?:Rua|Avenida|Av\.?|Travessa|Tv\.?|Praça|Pç\.?|Setor|Alameda|Rodovia|Estrada|Rod\.?|Via)\s+'
            r'[A-Za-zÀ-ÖØ-öø-ÿ0-9\s\.,º°\-]+(?:,\s*[A-Za-zÀ-ÖØ-öø-ÿ0-9\s\.,º°\-]+)*'
            r'(?:,\s*[A-Za-zÀ-ÖØ-öø-ÿ\s\-]+-[A-Z]{2})?\b',
            re.IGNORECASE | re.DOTALL
        ),
        "cep": re.compile(r'(\b\d{2}[\.\s]?\d{3})[\.\s-]*\d{3}\b', re.IGNORECASE | re.DOTALL),
        "cnpj": re.compile(r'\b\d{2}\s?\.\s?\d{3}\s?\.\s?\d{3}\s?/\s?\d{4}\s?-\s?\d{2}\b'),
    }

def redact_info_in_pdf(input_pdf_path, output_pdf_path, names_to_redact=None):
    patterns = get_default_patterns()

    if names_to_redact:
        for name in names_to_redact:
            name_pattern = re.escape(name).replace(r'\ ', r'\s*')
            pattern = re.compile(name_pattern, re.IGNORECASE | re.DOTALL)
            patterns[name] = pattern

    document = fitz.open(input_pdf_path)
    
    for page in document:
        text = page.get_text("text")

        for name, pattern in patterns.items():
            redact_pattern_in_text(page, text, pattern)

        page.apply_redactions()
    
    document.save(output_pdf_path)

def redact_pattern_in_text(page, text, pattern):
    matches = pattern.findall(text)
    
    for match in matches:
        if isinstance(match, tuple):
            match = match[0]
        
        areas = page.search_for(match)
        for area in areas:
            page.add_redact_annot(area, fill=(0, 0, 0))

def process_pdf(file_path, names_to_redact=None):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(PROCESSED_FOLDER):
        os.makedirs(PROCESSED_FOLDER)

    filename = secure_filename(os.path.basename(file_path))
    input_pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    output_pdf_filename = "processed_" + filename
    output_pdf_path = os.path.join(PROCESSED_FOLDER, output_pdf_filename)

    os.rename(file_path, input_pdf_path)

    try:
        redact_info_in_pdf(input_pdf_path, output_pdf_path, names_to_redact)
        print(f"PDF processado com sucesso! Arquivo salvo em: {output_pdf_path}")
    except Exception as e:
        print(f"Erro ao processar o PDF: {e}")

__name__ == "__main__"