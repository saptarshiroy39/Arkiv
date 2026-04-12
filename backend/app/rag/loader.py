from langchain_community.document_loaders import (
    CSVLoader,
    Docx2txtLoader,
    JSONLoader,
    PDFPlumberLoader,
    TextLoader,
    UnstructuredExcelLoader,
    UnstructuredImageLoader,
    UnstructuredMarkdownLoader,
    UnstructuredPowerPointLoader,
    WebBaseLoader,
)
from langchain_core.documents import Document


# PDF
# https://python.langchain.com/docs/integrations/document_loaders/pdfplumber
def read_pdf(path: str) -> list[Document]:
    loader = PDFPlumberLoader(path)
    docs = loader.load()
    return docs


# TXT
# https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.text.TextLoader
def read_txt(path: str) -> list[Document]:
    loader = TextLoader(path, encoding="utf-8")
    docs = loader.load()
    return docs


# CSV
# https://python.langchain.com/docs/integrations/document_loaders/csv
def read_csv(path: str) -> list[Document]:
    loader = CSVLoader(file_path=path)
    docs = loader.load()
    return docs


# MD
# https://python.langchain.com/docs/integrations/document_loaders/unstructured_file/
def read_md(path: str) -> list[Document]:
    loader = UnstructuredMarkdownLoader(path)
    docs = loader.load()
    return docs


# JSON
# https://python.langchain.com/docs/integrations/document_loaders/json
def read_json(path: str) -> list[Document]:
    loader = JSONLoader(file_path=path, jq_schema=".")
    docs = loader.load()
    return docs


# DOCX
# https://python.langchain.com/docs/integrations/document_loaders/microsoft_word
def read_docx(path: str) -> list[Document]:
    loader = Docx2txtLoader(path)
    docs = loader.load()
    return docs


# XLSX
# https://python.langchain.com/docs/integrations/document_loaders/microsoft_excel
def read_xlsx(path: str) -> list[Document]:
    loader = UnstructuredExcelLoader(path, mode="elements")
    docs = loader.load()
    return docs


# PPTX
# https://python.langchain.com/docs/integrations/document_loaders/microsoft_powerpoint
def read_pptx(path: str) -> list[Document]:
    loader = UnstructuredPowerPointLoader(path, mode="elements")
    docs = loader.load()
    return docs


# IMG
# https://python.langchain.com/docs/integrations/document_loaders/image
def read_img(path: str) -> list[Document]:
    loader = UnstructuredImageLoader(path)
    docs = loader.load()
    return docs


# URL
# https://python.langchain.com/docs/integrations/document_loaders/web_base
def read_url(url: str) -> list[Document]:
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs
