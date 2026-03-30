import pdfplumber

def read_pdf(path: str) -> list[dict]:
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            if text := (page.extract_text() or "").strip(): pages.append({"text": text})
    return pages
