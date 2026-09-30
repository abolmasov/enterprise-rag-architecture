from __future__ import annotations

from dataclasses import dataclass

from src.pipeline.chunking import chunk_text
from src.pipeline.index import InMemoryHybridIndex


@dataclass
class RagAnswer:
    answer: str
    citations: list[str]
    retrieved_chunk_ids: list[str]


class RagPipeline:
    def __init__(self) -> None:
        self.index = InMemoryHybridIndex()

    def ingest_text(self, doc_id: str, text: str) -> int:
        chunks = chunk_text(doc_id, text)
        for chunk in chunks:
            self.index.add(chunk)
        return len(chunks)

    def ask(self, question: str, top_k: int = 3) -> RagAnswer:
        hits = self.index.search(question, top_k=top_k)
        if not hits:
            return RagAnswer(
                answer="Insufficient grounded evidence.",
                citations=[],
                retrieved_chunk_ids=[],
            )
        context = " | ".join(h.chunk.text for h in hits)
        citations = [h.chunk.chunk_id for h in hits]
        answer = f"Based on indexed policy context: {context}"
        return RagAnswer(answer=answer, citations=citations, retrieved_chunk_ids=citations)
