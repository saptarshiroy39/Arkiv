from langchain_core.documents import Document

from app.rag.cleaner import clean_text, process_latex
from app.rag.chunker import chunk_docs
from app.rag.vectorstore import add_documents
from app.rag.loader import (
    read_csv,
    read_docx,
    read_img,
    read_json,
    read_md,
    read_pdf,
    read_pptx,
    read_txt,
    read_url,
    read_xlsx,
)

LOADERS = {
    "pdf": read_pdf,
    "txt": read_txt,
    "csv": read_csv,
    "md": read_md,
    "json": read_json,
    "docx": read_docx,
    "xlsx": read_xlsx,
    "pptx": read_pptx,
    "img": read_img,
    "png": read_img,
    "jpg": read_img,
    "jpeg": read_img,
}


def _clean_docs(docs: list[Document]) -> list[Document]:
    for doc in docs:
        doc.page_content = clean_text(doc.page_content)
        doc.page_content = process_latex(doc.page_content)
    return docs


def process_file(path: str, ext: str) -> int:
    loader = LOADERS.get(ext.lower())
    if loader is None:
        raise ValueError(f"Unsupported file type: .{ext}")
    docs = loader(path)
    docs = _clean_docs(docs)
    chunks = chunk_docs(docs)
    add_documents(chunks)
    return len(chunks)


def process_url(url: str) -> int:
    docs = read_url(url)
    docs = _clean_docs(docs)
    chunks = chunk_docs(docs)
    add_documents(chunks)
    return len(chunks)


# Manual
