"""EduRAG 问答后端：检索增强生成（RAG）API。

提供：
  GET  /api/health            健康检查
  POST /api/documents         新增文档（自动分块入索引）
  GET  /api/documents         文档列表
  DELETE /api/documents/{id}  删除文档
  POST /api/chat              同步问答（便于测试 / 非流式场景）
  POST /api/chat/stream       流式问答（SSE，前端对话页使用）
  GET  /api/history/{sid}     会话历史
"""
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import config
from .llm import get_llm
from .retriever import retriever
from .store import store, seed_demo

app = FastAPI(title="EduRAG QA", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 演示用；生产改为前端域名
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- 请求模型 ----------
class DocIn(BaseModel):
    title: str
    text: str


class ChatIn(BaseModel):
    question: str
    session_id: str | None = None
    top_k: int = 5


# ---------- 启动 ----------
@app.on_event("startup")
def startup() -> None:
    seed_demo()
    retriever.mark_dirty()


# ---------- 文档管理 ----------
@app.get("/api/documents")
def list_documents():
    return [{"id": d.id, "title": d.title,
             "chunk_count": d.chunk_count,
             "created_at": d.created_at} for d in store.list_documents()]


@app.post("/api/documents", status_code=201)
def add_document(doc: DocIn):
    if not doc.title.strip() or not doc.text.strip():
        raise HTTPException(400, "title 与 text 不能为空")
    d = store.add_document(doc.title, doc.text)
    retriever.mark_dirty()
    return {"id": d.id, "title": d.title, "chunk_count": d.chunk_count}


@app.delete("/api/documents/{doc_id}")
def delete_document(doc_id: int):
    if not store.delete_document(doc_id):
        raise HTTPException(404, "文档不存在")
    retriever.mark_dirty()
    return {"ok": True}


# ---------- 问答 ----------
def _answer(question: str, session_id: str | None, top_k: int):
    session_id = store.ensure_session(session_id)
    results = retriever.search(question, top_k=top_k)
    confidence = results[0]["score"] if results else 0.0
    can_answer = confidence >= config.FAQ_THRESHOLD
    store.add_message(session_id, "user", question)
    return results, confidence, can_answer, session_id


@app.post("/api/chat")
async def chat(chat_in: ChatIn):
    results, confidence, can_answer, session_id = _answer(
        chat_in.question, chat_in.session_id, chat_in.top_k)
    llm = get_llm()
    parts = []
    async for tok in llm.stream_answer(chat_in.question, results, can_answer):
        parts.append(tok)
    answer = "".join(parts)
    store.add_message(session_id, "assistant", answer)
    return {
        "session_id": session_id,
        "answer": answer,
        "docs": results,
        "confidence": confidence,
        "can_answer": can_answer,
    }


@app.post("/api/chat/stream")
async def chat_stream(chat_in: ChatIn):
    results, confidence, can_answer, session_id = _answer(
        chat_in.question, chat_in.session_id, chat_in.top_k)
    llm = get_llm()

    async def event_gen():
        yield _sse({"type": "meta", "session_id": session_id,
                    "confidence": confidence, "can_answer": can_answer})
        yield _sse({"type": "sources", "docs": results})
        answer_parts = []
        async for tok in llm.stream_answer(chat_in.question, results, can_answer):
            answer_parts.append(tok)
            yield _sse({"type": "token", "text": tok})
        store.add_message(session_id, "assistant", "".join(answer_parts))
        yield _sse({"type": "done"})

    return await _stream_response(event_gen())


def _sse(obj: dict) -> str:
    return f"data: {json.dumps(obj, ensure_ascii=False)}\n\n"


async def _stream_response(gen):
    from fastapi.responses import StreamingResponse
    return StreamingResponse(gen, media_type="text/event-stream",
                            headers={"Cache-Control": "no-cache",
                                     "X-Accel-Buffering": "no"})


# ---------- 历史 ----------
@app.get("/api/history/{session_id}")
def history(session_id: str, limit: int = 50):
    return {"session_id": session_id, "messages": store.get_history(session_id, limit)}


@app.get("/api/health")
def health():
    return {"status": "ok", "llm_mode": config.LLM_MODE,
            "embedding_mode": config.EMBEDDING_MODE,
            "faq_threshold": config.FAQ_THRESHOLD}
