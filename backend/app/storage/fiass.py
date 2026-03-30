import os, shutil
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import EMBED_MODEL, GOOGLE_API_KEY

PATH = os.path.join("data", "vectorstores", "default_index")

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(model=EMBED_MODEL, google_api_key=GOOGLE_API_KEY)

def get_vectorstore():
    if os.path.exists(PATH):
        return FAISS.load_local(PATH, get_embeddings(), allow_dangerous_deserialization=True)
    return None

def add_documents(chunks: list):
    store = get_vectorstore()
    if store: store.add_documents(chunks)
    else: store = FAISS.from_documents(chunks, get_embeddings())
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    store.save_local(PATH)

def delete_vectorstore() -> bool:
    if os.path.exists(PATH):
        shutil.rmtree(PATH)
        return True
    return False
