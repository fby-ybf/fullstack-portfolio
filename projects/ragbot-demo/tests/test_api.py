"""测试：覆盖检索排序、未命中、问答接口。"""
from fastapi.testclient import TestClient

from app.knowledge import build_kb
from app.main import app
from app.retriever import KnowledgeBase

client = TestClient(app)


def test_search_returns_relevant_top():
    kb = build_kb()
    hits = kb.search("栈是什么数据结构")
    assert hits
    assert "栈" in hits[0].chunk.text


def test_search_orders_by_score():
    kb = build_kb()
    hits = kb.search("二叉树的遍历")
    assert hits[0].score >= hits[-1].score


def test_threshold_filters_irrelevant():
    kb = KnowledgeBase(threshold=0.5)
    kb.add("栈是后进先出的数据结构")
    hits = kb.search("完全无关的另一个主题xyz")
    assert hits == []


def test_ask_endpoint():
    r = client.post("/api/ask", json={"question": "队列的特点是什么"})
    assert r.status_code == 200
    body = r.json()
    assert body["answer"]
    assert body["hits"]


def test_ask_no_hit_still_answers():
    r = client.post("/api/ask", json={"question": "今天天气怎么样"})
    assert r.status_code == 200
    body = r.json()
    assert body["hits"] == []  # 无相关片段
    assert body["answer"]  # 仍返回一个「资料未提及」的兜底回答


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
