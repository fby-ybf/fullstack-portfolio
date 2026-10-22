from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert 0 < body["faq_threshold"] <= 1


def test_add_and_list_document():
    r = client.post("/api/documents", json={
        "title": "单元测试文档",
        "text": "如何申请发票？在订单详情页点击申请发票，填写抬头后提交，电子发票将发送至邮箱。",
    })
    assert r.status_code == 201
    doc_id = r.json()["id"]

    lst = client.get("/api/documents").json()
    assert any(d["id"] == doc_id for d in lst)

    # 删除
    d = client.delete(f"/api/documents/{doc_id}")
    assert d.status_code == 200
    lst2 = client.get("/api/documents").json()
    assert all(x["id"] != doc_id for x in lst2)


def test_chat_sync_returns_structure():
    r = client.post("/api/chat", json={"question": "怎么重置密码？"})
    assert r.status_code == 200
    body = r.json()
    assert "answer" in body and "docs" in body
    assert isinstance(body["can_answer"], bool)
    assert 0 <= body["confidence"] <= 1
    assert body["session_id"]


def test_chat_stream_is_sse():
    r = client.post("/api/chat/stream", json={"question": "支持哪些登录方式？"})
    assert r.status_code == 200
    text = r.text
    assert "data:" in text
    assert "type" in text           # 事件里带 type 字段
    assert "token" in text          # 至少流式吐过字


def test_history_records_messages():
    sid = client.post("/api/chat", json={"question": "退款多久到账？"}).json()["session_id"]
    h = client.get(f"/api/history/{sid}").json()
    assert len(h["messages"]) >= 2   # user + assistant
    roles = [m["role"] for m in h["messages"]]
    assert "user" in roles and "assistant" in roles
