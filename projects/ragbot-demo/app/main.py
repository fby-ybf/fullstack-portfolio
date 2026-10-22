"""FastAPI 入口：问答接口 + 静态页面。"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .generator import FakeLLM, generate_answer
from .knowledge import build_kb
from .retriever import SearchHit

kb = build_kb()
llm = FakeLLM()

app = FastAPI(title="课程答疑 RAG 演示", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str
    top_k: int = 3


class HitOut(BaseModel):
    score: float
    text: str


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]
    hits: list[HitOut]


@app.post("/api/ask", response_model=AskResponse)
def ask(req: AskRequest):
    hits: list[SearchHit] = kb.search(req.question, top_k=req.top_k)
    ans = generate_answer(req.question, hits, llm)
    return {
        "question": req.question,
        "answer": ans.text,
        "sources": ans.sources,
        "hits": [
            {"score": round(h.score, 4), "text": h.chunk.text} for h in hits
        ],
    }


@app.get("/api/health")
def health():
    return {"status": "ok", "chunks": len(kb._chunks)}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
