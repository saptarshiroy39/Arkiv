from app.config import CHAT_MODEL, GOOGLE_API_KEY, PROMPT, TOP_K
from app.rag.vectorstore import get_vectorstore
from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

router = APIRouter()


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]

@router.post("/ask")
async def ask(body: AskRequest) -> AskResponse:
    store = get_vectorstore()
    if not store:
        raise HTTPException(404, "No documents ingested yet.")

    docs = store.similarity_search(body.question, k=TOP_K)
    context = "\n\n".join(d.page_content for d in docs)
    sources = list({d.metadata.get("source", "unknown") for d in docs})

    llm = ChatGoogleGenerativeAI(model=CHAT_MODEL, google_api_key=GOOGLE_API_KEY)
    response = llm.invoke([HumanMessage(content=PROMPT.format(context=context, question=body.question))])

    return AskResponse(answer=response.content, sources=sources)
