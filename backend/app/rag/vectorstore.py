import os
import shutil

from langchain_community.vectorstores import FAISS
from app.rag.embedder import embeddings

PATH = "data/vectorstores/default_index"


def get_vectorstore():
    if os.path.exists(PATH):
        return FAISS.load_local(
            PATH, embeddings, allow_dangerous_deserialization=True
        )
    return None


def add_documents(chunks):
    store = get_vectorstore()

    if store:
        store.add_documents(chunks)
    else:
        store = FAISS.from_documents(chunks, embeddings)

    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    store.save_local(PATH)


def delete_vectorstore():
    if os.path.exists(PATH):
        shutil.rmtree(PATH)
        return True
    return False

# Antigravity -> Claude Sonnet 4.6 (Thinking)