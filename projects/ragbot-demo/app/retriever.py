"""知识库检索：把「检索」与「生成」拆成两个可独立测试的环节。

设计要点（面试可讲）：
- 检索只负责「从知识库找出最相关的片段」，不碰大模型；
- 相似度用余弦相似度（词袋 + TF 加权），纯 Python 实现、零外部依赖，
  换真实 embedding/向量库时只替换 score 函数，接口不变。
- 设置召回阈值：低于阈值视为「未命中」，避免把无关片段塞给大模型。
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass

# 英文分词 + 中文按单字切分，简单够用
_TOKEN = re.compile(r"[a-z0-9]+|[\u4e00-\u9fff]")


def _tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def _tf_vector(tokens: list[str]) -> dict[str, float]:
    vec: dict[str, float] = {}
    for t in tokens:
        vec[t] = vec.get(t, 0.0) + 1.0
    return vec


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    common = set(a) & set(b)
    dot = sum(a[k] * b[k] for k in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


@dataclass
class Chunk:
    id: int
    text: str


@dataclass
class SearchHit:
    chunk: Chunk
    score: float


class KnowledgeBase:
    """内存知识库：存文本片段，按查询返回最相关片段。"""

    def __init__(self, threshold: float = 0.1):
        self.threshold = threshold
        self._chunks: list[Chunk] = []
        self._index: list[dict[str, float]] = []

    def add(self, text: str) -> None:
        chunk = Chunk(id=len(self._chunks), text=text)
        self._chunks.append(chunk)
        self._index.append(_tf_vector(_tokenize(text)))

    def search(self, query: str, top_k: int = 3) -> list[SearchHit]:
        qvec = _tf_vector(_tokenize(query))
        scored = []
        for i, cvec in enumerate(self._index):
            s = _cosine(qvec, cvec)
            if s >= self.threshold:
                scored.append(SearchHit(self._chunks[i], s))
        scored.sort(key=lambda h: h.score, reverse=True)
        return scored[:top_k]
