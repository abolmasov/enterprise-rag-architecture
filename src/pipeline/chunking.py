from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Chunk:
    doc_id: str
    chunk_id: str
    text: str
    metadata: dict


def chunk_text(doc_id: str, text: str, size: int = 200, overlap: int = 40) -> list[Chunk]:
    words = text.split()
    chunks: list[Chunk] = []
    start = 0
    idx = 0
    while start < len(words):
        end = min(len(words), start + size)
        piece = " ".join(words[start:end])
        chunks.append(
            Chunk(
                doc_id=doc_id,
                chunk_id=f"{doc_id}:{idx}",
                text=piece,
                metadata={"start_word": start, "end_word": end},
            )
        )
        if end == len(words):
            break
        start = max(0, end - overlap)
        idx += 1
    return chunks
