"""Okapi BM25 召回（从零实现，无第三方依赖）。

与向量召回组成"双路召回"，再在 retriever 里做融合排序（RRF + 加权）。
"""
import math
from collections import Counter

from .embeddings import tokenize


class BM25:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.docs: list[list[str]] = []
        self.doc_ids: list[int] = []
        self.idf: dict[str, float] = {}
        self.avgdl: float = 0.0

    def fit(self, docs: list[dict]) -> None:
        self.docs = [tokenize(d["text"]) for d in docs]
        self.doc_ids = [d["id"] for d in docs]
        n = len(self.docs)
        df: dict[str, int] = {}
        lengths = []
        for toks in self.docs:
            lengths.append(len(toks))
            for t in set(toks):
                df[t] = df.get(t, 0) + 1
        self.idf = {
            t: math.log((n - f + 0.5) / (f + 0.5) + 1.0) for t, f in df.items()
        }
        self.avgdl = sum(lengths) / n if n else 0.0

    def search(self, query: str, top_k: int = 5) -> list[tuple[int, float]]:
        if not self.docs:
            return []
        q_tokens = tokenize(query)
        scores = []
        for idx, doc in enumerate(self.docs):
            dl = len(doc)
            freq = Counter(doc)
            score = 0.0
            for t in q_tokens:
                if t not in freq:
                    continue
                idf = self.idf.get(t, 0.0)
                f = freq[t]
                denom = f + self.k1 * (1 - self.b + self.b * (dl / self.avgdl if self.avgdl else 1))
                score += idf * (f * (self.k1 + 1)) / denom
            scores.append((self.doc_ids[idx], score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
