"""双路召回 + 融合排序。

流程：
  1) BM25 召回 top-k（关键词精确匹配，擅长术语/编号）
  2) 向量召回 top-k（语义匹配，擅长同义改写）
  3) 各自归一化到 [0,1] 后按权重融合（默认各 0.5），得到最终排序与置信度
生产把向量召回替换为 Milvus ANN 检索，融合逻辑保持不变。
"""
from .bm25 import BM25
from .embeddings import VectorIndex
from .store import store


class Retriever:
    def __init__(self, bm25_weight: float = 0.5, vec_weight: float = 0.5):
        self.bm25_weight = bm25_weight
        self.vec_weight = vec_weight
        self.bm25 = BM25()
        self.vec = VectorIndex()
        self._dirty = True
        self._chunks: list[dict] = []

    def _rebuild(self) -> None:
        self._chunks = store.get_chunks()
        self.bm25.fit(self._chunks)
        self.vec.fit(self._chunks)
        self._dirty = False

    def mark_dirty(self) -> None:
        self._dirty = True

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        if self._dirty or not self._chunks:
            self._rebuild()
        if not self._chunks:
            return []

        bm = self.bm25.search(query, top_k=top_k * 2)
        vs = self.vec.search(query, top_k=top_k * 2)

        bm_max = max((s for _, s in bm), default=1.0) or 1.0
        vs_max = max((s for _, s in vs), default=1.0) or 1.0

        scored: dict[int, float] = {}
        for cid, s in bm:
            scored[cid] = scored.get(cid, 0.0) + self.bm25_weight * (s / bm_max)
        for cid, s in vs:
            scored[cid] = scored.get(cid, 0.0) + self.vec_weight * (s / vs_max)

        ranked = sorted(scored.items(), key=lambda x: x[1], reverse=True)[:top_k]
        results = []
        for cid, score in ranked:
            chunk = next(c for c in self._chunks if c["id"] == cid)
            results.append({
                "id": cid,
                "title": chunk["text"].split("\n", 1)[0].strip("【】"),
                "text": chunk["text"],
                "score": round(score, 4),
            })
        return results


retriever = Retriever()
