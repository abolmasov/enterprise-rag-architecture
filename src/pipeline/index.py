from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from src.pipeline.chunking import Chunk


@dataclass
class SearchHit:
    chunk: Chunk
    score: float


@dataclass
class InMemoryHybridIndex:
    chunks: dict[str, Chunk] = field(default_factory=dict)
    inverted: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))

    def add(self, chunk: Chunk) -> None:
        self.chunks[chunk.chunk_id] = chunk
        for token in set(chunk.text.lower().split()):
            self.inverted[token].add(chunk.chunk_id)

    def search(self, query: str, top_k: int = 5) -> list[SearchHit]:
        tokens = set(query.lower().split())
        scores: dict[str, float] = defaultdict(float)
        for token in tokens:
            for chunk_id in self.inverted.get(token, set()):
                scores[chunk_id] += 1.0
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [SearchHit(chunk=self.chunks[cid], score=score) for cid, score in ranked]
