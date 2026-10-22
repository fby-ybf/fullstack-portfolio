"""可插拔 LLM 生成层。

- fake：离线演示，无需任何密钥，按字符流式吐字，并尊重 can_answer 标志做"拒答"。
- openai：接入真实大模型（LLM_MODE=openai），openai 库按需安装，缺失时自动回退 fake。

生成时把检索到的片段作为上下文，并标注来源，降低幻觉。
"""
import asyncio

from . import config


async def _fake_stream(text: str, delay: float = 0.01):
    for ch in text:
        yield ch
        await asyncio.sleep(delay)


class FakeLLM:
    async def stream_answer(self, question: str, docs: list[dict], can_answer: bool):
        if not can_answer:
            yield "抱歉，知识库中未检索到与该问题足够相关的确切信息（置信度低于阈值）。"
            yield "建议：1）补充相关文档后重试；2）联系人工客服获取准确答复。"
            return
        ctx = "；".join(d["text"].replace("\n", " ") for d in docs[:3])
        answer = (
            f"根据知识库内容，关于「{question}」的答复如下：\n"
            f"{ctx}\n"
            f"\n（以上回答由检索增强生成，仅供参考，来源见右侧引用。）"
        )
        async for ch in _fake_stream(answer):
            yield ch


class OpenAILLM:
    def __init__(self):
        # 延迟导入，避免无密钥环境也必须安装 openai
        try:
            from openai import AsyncOpenAI  # noqa
            self.client = AsyncOpenAI(api_key=config.OPENAI_API_KEY,
                                      base_url=config.OPENAI_BASE_URL or None)
        except Exception:
            self.client = None

    async def stream_answer(self, question: str, docs: list[dict], can_answer: bool):
        if self.client is None:
            async for ch in FakeLLM().stream_answer(question, docs, can_answer):
                yield ch
            return
        if not can_answer:
            async for ch in FakeLLM().stream_answer(question, docs, can_answer):
                yield ch
            return
        ctx = "；".join(d["text"].replace("\n", " ") for d in docs[:3])
        prompt = (
            "你是企业客服助手，仅依据下方【知识库】内容作答，"
            "若内容不足以回答请直接说不知道，不要编造。\n"
            f"【知识库】{ctx}\n【用户问题】{question}\n【回答】"
        )
        try:
            stream = await self.client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
            async for part in stream:
                delta = part.choices[0].delta.content or ""
                if delta:
                    yield delta
        except Exception:
            async for ch in FakeLLM().stream_answer(question, docs, can_answer):
                yield ch


def get_llm():
    if config.LLM_MODE == "openai":
        return OpenAILLM()
    return FakeLLM()
