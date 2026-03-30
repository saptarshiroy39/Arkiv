from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import CHAT_MODEL, GOOGLE_API_KEY, TOP_K
from app.storage.fiass import get_vectorstore

class AskRequest(BaseModel): text: str

router = APIRouter()

PROMPT = """You are Arkiv, a helpful document assistant.
Answer the question based ONLY on the provided context.
If the context contains math or LaTeX, preserve them using $ for inline and $$ for display math.
If you cannot answer from the context, say so honestly.

Context:
{context}

Question: {question}"""

@router.post("/ask")
async def ask(body: AskRequest):
    try:
        store = get_vectorstore()
        if not store: return {"text": "No documents uploaded yet."}
            
        docs = await asyncio.to_thread(store.similarity_search, body.text, k=TOP_K)
        if not docs: return {"text": "No relevant documents found."}

        context = "\n\n".join(d.page_content for d in docs)
        
        llm = ChatGoogleGenerativeAI(model=CHAT_MODEL, google_api_key=GOOGLE_API_KEY, max_retries=3)
        answer = await asyncio.to_thread(llm.invoke, PROMPT.format(context=context, question=body.text))

        return {"text": answer.content}
    except Exception as e: 
        raise HTTPException(500, str(e))
