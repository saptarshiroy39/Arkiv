import os, asyncio, re
from fastapi import APIRouter, HTTPException
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import CHUNK_OVERLAP, CHUNK_SIZE
from app.readers.csv import read_csv
from app.readers.docx import read_docx
from app.readers.excel import read_excel
from app.readers.pdf import read_pdf
from app.readers.pptx import read_pptx
from app.readers.text import read_text
from app.storage.fiass import add_documents

router = APIRouter()
READERS = {
    "pdf": read_pdf,
    "docx": read_docx,
    "xlsx": read_excel,
    "csv": read_csv,
    "pptx": read_pptx,
    "txt": read_text,
    "md": read_text,
    "json": read_text,
}
splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
)


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\x00", "")
    return re.sub(r" {2,}|\t+", " ", re.sub(r"\n{3,}", "\n\n", text)).strip()


def process_latex(text: str) -> str:
    if not text:
        return text
    text = re.sub(r"\\\[(.*?)\\\]", r"$$\1$$", text, flags=re.DOTALL)
    text = re.sub(r"\\\((.*?)\\\)", r"$\1$", text, flags=re.DOTALL)
    display = r"equation|align|gather|displaymath|eqnarray|multline|flalign|split"
    text = re.sub(rf"\\begin{{({display})\*?}}(.*?)\\end{{\1\*?}}", r"$$\2$$", text, flags=re.DOTALL)
    matrix = r"matrix|pmatrix|bmatrix|vmatrix|Bmatrix|cases|array"
    text = re.sub(rf"(?<!\$)\\begin{{({matrix})\*?}}(.*?)\\end{{\1\*?}}", r"$$\\begin{\1}\2\\end{\1}$$", text, flags=re.DOTALL)
    return re.sub(r"\${3,}", "$$", text)


async def _embed_file(path: str, filename: str):
    ext = filename.split(".")[-1].lower() if "." in filename else ""

    if ext not in READERS:
        raise ValueError(f"Unsupported: {filename}")

    data = await asyncio.to_thread(READERS[ext], path)

    docs = []
    for item in data:
        cleaned_text = process_latex(clean_text(item["text"]))
        if cleaned_text:
            docs.append(
                Document(page_content=cleaned_text)
            )

    if not docs:
        return {"file": filename, "chunks": 0}

    chunks = splitter.split_documents(docs)
    await asyncio.to_thread(add_documents, chunks)
    return {"file": filename, "chunks": len(chunks)}


@router.post("/process")
async def process():
    files = (
        [f for f in os.listdir("data/staging")]
        if os.path.exists("data/staging")
        else []
    )
    if not files:
        raise HTTPException(400, "Upload files first")

    processed, errors = [], []
    for f in files:
        path = os.path.join("data/staging", f)
        try:
            processed.append(await _embed_file(path, f))
        except Exception as e:
            errors.append({"file": f, "error": str(e)[:200]})
        finally:
            if os.path.exists(path):
                os.unlink(path)

    return {
        "processed": processed,
        "errors": errors,
        "message": f"{len(processed)} ok, {len(errors)} fail",
    }
