from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import CHUNK_SIZE, CHUNK_OVERLAP

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
)


def chunk_docs(docs: list[Document]) -> list[Document]:
    return text_splitter.split_documents(docs)


# https://docs.langchain.com/oss/python/integrations/splitters
