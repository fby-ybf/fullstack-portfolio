"""轻量向量召回（纯 numpy，零外部模型依赖）。

说明：演示用 TF-IDF 余弦相似度做"向量召回"，目的是让项目零依赖即可跑通双路召回。
生产环境把 EMBEDDING_MODE 切到 milvus，由 embed() 替换为真实句向量（如 bge/sentence-transformers），
检索逻辑不变。

中文分词采用"ASCII 词 + CJK 单字"混合策略，便于中文片段的字符级重合匹配。
"""
import math
import re

import numpy as np


def tokenize(text: str) -> list[str]:
    text = (text or "").lower()
    tokens = re.findall(r"[a-z0-9]+", text)          # 英文/数字词
    tokens += re.findall(r"[一-鿿]", text)            # 中文按单字切（演示用）
    return tokens


class VectorIndex:
    def __init__(self):
        self.vocab: dict[str, int] = {}
        self.idf: np.ndarray | None = None
        self.doc_vectors: list[np.ndarray] = []
        self.doc_ids: list[int] = []

    def _vectorize(self, tokens: list[str]) -> np.ndarray:
        v = np.zeros(len(self.vocab), dtype=np.float32)
        for t in tokens:
            if t in self.vocab:
                v[self.vocab[t]] += 1.0
        if v.sum() == 0:
            return v
        # tf-idf
        v = v * self.idf
        norm = np.linalg.norm(v)
        if norm > 0:
            v = v / norm
        return v

    def fit(self, docs: list[dict]) -> None:
        """docs: [{'id': int, 'text': str}, ...]"""
        df: dict[str, int] = {}
        tokenized: list[list[str]] = []
        for d in docs:
            toks = tokenize(d["text"])
            tokenized.append(toks)
            for t in set(toks):
                df[t] = df.get(t, 0) + 1
        self.vocab = {t: i for i, t in enumerate(sorted(df.keys()))}
        n = len(docs)
        self.idf = np.array(
            [math.log((1 + n) / (1 + df[t])) + 1.0 for t in sorted(df.keys())],
            dtype=np.float32,
        )
        self.doc_ids = [d["id"] for d in docs]
        self.doc_vectors = [self._vectorize(toks) for toks in tokenized]

    def search(self, query: str, top_k: int = 5) -> list[tuple[int, float]]:
        if not self.doc_vectors:
            return []
        q = self._vectorize(tokenize(query))
        if q.sum() == 0:
            return []
        sims = np.array([float(np.dot(q, dv)) for dv in self.doc_vectors], dtype=np.float32)
        sims = np.clip(sims, 0.0, 1.0)
        order = np.argsort(-sims)[:top_k]
        return [(self.doc_ids[i], float(sims[i])) for i in order]
