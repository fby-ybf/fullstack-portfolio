"""接口测试：用 TestClient 直接跑真实路由（不 mock 数据库）。"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_students():
    r = client.get("/api/students")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(s["student_no"] == "20230001" for s in data)


def test_filter_by_class():
    r = client.get("/api/students", params={"clazz": "计科2301"})
    assert r.status_code == 200
    assert all(s["clazz"] == "计科2301" for s in r.json())


def test_student_scores():
    r = client.get("/api/students/20230001/scores")
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "张三"
    assert len(body["scores"]) == 2


def test_student_not_found():
    r = client.get("/api/students/99999/scores")
    assert r.status_code == 404


def test_class_stats():
    r = client.get("/api/stats/classes")
    assert r.status_code == 200
    assert any(c["clazz"] == "计科2301" for c in r.json())


def test_pagination_limit_bounds():
    # limit 超上限应被 422 拒绝（Query le=100 校验）
    r = client.get("/api/students", params={"limit": 999})
    assert r.status_code == 422
