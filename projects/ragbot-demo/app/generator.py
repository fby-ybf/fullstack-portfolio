"""生成环节：把检索到的片段拼进 prompt，交给大模型。

设计要点：
- 大模型调用做成可插拔：默认用 FakeLLM（确定性输出，便于测试），
  接真实大模型时实现同接口的 RealLLM 即可。
- prompt 里显式要求「只基于给定资料回答，资料没有就说不确定」，
  这是 RAG 减少「幻觉」的关键约束。
- 把引用来源一起返回，让答案可追溯。
"""
from __future__ import annotations

from dataclasses import dataclass

from .retriever import SearchHit


@dataclass
class Answer:
    text: str
    sources: list[str]


class LLM:
    """大模型抽象接口。"""

    def generate(self, prompt: str) -> str:
        raise NotImplementedError


class FakeLLM(LLM):
    """演示用假模型：返回拼接了资料片段的固定文本，方便测试。"""

    def generate(self, prompt: str) -> str:
        return f"[demo 模型输出] 基于以下资料回答：\n{prompt[-200:]}"


def build_prompt(query: str, hits: list[SearchHit]) -> str:
    context = "\n".join(f"[{i+1}] {h.chunk.text}" for i, h in enumerate(hits))
    return (
        "你是课程答疑助手。只依据下面的资料回答，资料里没有的内容请回答「资料中未提及」，"
        "不要编造。\n\n资料：\n"
        f"{context}\n\n"
        f"问题：{query}\n"
    )


def generate_answer(query: str, hits: list[SearchHit], llm: LLM) -> Answer:
    prompt = build_prompt(query, hits)
    text = llm.generate(prompt)
    sources = [f"片段{h.chunk.id + 1}" for h in hits]
    return Answer(text=text, sources=sources)
