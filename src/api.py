from fastapi import FastAPI
from pydantic import BaseModel

from src.pipeline.rag import RagAnswer, RagPipeline

app = FastAPI(title="Enterprise RAG Architecture", version="0.1.0")
rag = RagPipeline()


class IngestRequest(BaseModel):
    doc_id: str
    text: str


class AskRequest(BaseModel):
    question: str
    top_k: int = 3


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ingest")
def ingest(req: IngestRequest) -> dict[str, int]:
    count = rag.ingest_text(req.doc_id, req.text)
    return {"chunks": count}


@app.post("/ask", response_model=RagAnswer)
def ask(req: AskRequest) -> RagAnswer:
    return rag.ask(req.question, top_k=req.top_k)
