import os
# pyrefly: ignore [missing-import]
from pypdf import PdfReader
# pyrefly: ignore [missing-import]
import docx

def parse_txt(file_bytes: bytes) -> str:
    return file_bytes.decode('utf-8', errors='ignore')

def parse_pdf(file_bytes: bytes) -> str:
    from io import BytesIO
    reader = PdfReader(BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def parse_docx(file_bytes: bytes) -> str:
    from io import BytesIO
    doc = docx.Document(BytesIO(file_bytes))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_file(filename: str, file_bytes: bytes) -> str:
    ext = os.path.splitext(filename)[1].lower()
    if ext == '.pdf':
        return parse_pdf(file_bytes)
    elif ext == '.docx':
        return parse_docx(file_bytes)
    elif ext == '.txt':
        return parse_txt(file_bytes)
    else:
        raise ValueError(f"Unsupported file extension: {ext}. Only .txt, .pdf, and .docx are supported.")
