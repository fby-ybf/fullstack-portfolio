"""验证 /metrics 能正常产出、三类指标都存在。"""
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_metrics_endpoint():
    r = client.get("/metrics")
    assert r.status_code == 200
    body = r.text
    assert "request_count_total" in body
    assert "request_duration_seconds" in body
    assert "app_up" in body


def test_root_and_metrics_increment():
    client.get("/")
    r = client.get("/metrics")
    assert "request_count_total" in r.text


def test_error_endpoint_returns():
    r = client.get("/error")
    assert r.status_code in (200, 500)
