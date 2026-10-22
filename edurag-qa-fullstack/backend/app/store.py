"""内存知识库与会话存储。

演示用内存实现；生产替换为 Milvus（向量）+ MySQL/ES（文档元数据）+ Redis（会话）。
提供文档 → 分块 的管理，以及会话历史的存取。
"""
import re
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Chunk:
    id: int
    doc_id: int
    title: str
    text: str


@dataclass
class Document:
    id: int
    title: str
    created_at: float
    chunk_count: int


@dataclass
class Message:
    role: str          # user / assistant
    content: str
    ts: float


class Store:
    def __init__(self):
        self._doc_id = 0
        self._chunk_id = 0
        self.documents: dict[int, Document] = {}
        self.chunks: list[Chunk] = []
        self.conversations: dict[str, list[Message]] = {}

    # ---- 文档 / 分块 ----
    def add_document(self, title: str, text: str) -> Document:
        self._doc_id += 1
        doc_id = self._doc_id
        for piece in self._split(text):
            self._chunk_id += 1
            self.chunks.append(Chunk(id=self._chunk_id, doc_id=doc_id,
                                     title=title, text=piece))
        doc = Document(id=doc_id, title=title, created_at=time.time(),
                       chunk_count=self._count_chunks(doc_id))
        self.documents[doc_id] = doc
        return doc

    def _count_chunks(self, doc_id: int) -> int:
        return sum(1 for c in self.chunks if c.doc_id == doc_id)

    @staticmethod
    def _split(text: str, size: int = 200, overlap: int = 40) -> list[str]:
        text = re.sub(r"\s+", " ", (text or "").strip())
        if not text:
            return []
        if len(text) <= size:
            return [text]
        pieces = []
        start = 0
        while start < len(text):
            pieces.append(text[start:start + size])
            start += size - overlap
        return pieces

    def list_documents(self) -> list[Document]:
        return sorted(self.documents.values(), key=lambda d: d.id)

    def delete_document(self, doc_id: int) -> bool:
        if doc_id not in self.documents:
            return False
        self.documents.pop(doc_id)
        self.chunks = [c for c in self.chunks if c.doc_id != doc_id]
        return True

    def get_chunks(self) -> list[dict]:
        return [{"id": c.id, "text": f"【{c.title}】\n{c.text}"} for c in self.chunks]

    # ---- 会话历史 ----
    def ensure_session(self, session_id: Optional[str] = None) -> str:
        if not session_id:
            session_id = str(uuid.uuid4())
        self.conversations.setdefault(session_id, [])
        return session_id

    def add_message(self, session_id: str, role: str, content: str) -> None:
        self.conversations.setdefault(session_id, []).append(
            Message(role=role, content=content, ts=time.time())
        )

    def get_history(self, session_id: str, limit: int = 50) -> list[dict]:
        msgs = self.conversations.get(session_id, [])
        return [{"role": m.role, "content": m.content} for m in msgs[-limit:]]


store = Store()


def seed_demo() -> None:
    """首次启动写入一份示例 FAQ，让对话开箱即用。"""
    if store.documents:
        return
    store.add_document(
        "产品使用 FAQ",
        "Q: 如何重置密码？ A: 在登录页点击'忘记密码'，通过注册邮箱接收验证码后设置新密码。"
        "Q: 支持哪些登录方式？ A: 支持邮箱、手机号验证码以及企业微信扫码登录。"
        "Q: 数据如何导出？ A: 在'个人中心-数据管理'中选择导出格式（CSV / Excel），系统将在后台生成下载链接。",
    )
    store.add_document(
        "退款政策",
        "Q: 退款多久到账？ A: 审核通过后，原路退回，通常 1-3 个工作日到账。"
        "Q: 哪些情况不支持退款？ A: 虚拟商品已兑换、定制化服务已开始交付的订单不支持退款。",
    )
