from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/api/health").json()["status"] == "ok"


def test_metrics_endpoint_exposes_custom_metric():
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "monitor_requests_total" in r.text


def test_webhook_receives_and_lists_alerts():
    payload = {
        "status": "firing",
        "alerts": [
            {
                "status": "firing",
                "labels": {"alertname": "HighCpu", "severity": "warning", "instance": "web-01"},
                "annotations": {"summary": "CPU 使用率过高"},
                "fingerprint": "abc123",
            }
        ],
    }
    wr = client.post("/api/alerts/webhook", json=payload)
    assert wr.status_code == 200
    assert wr.json()["received"] == 1

    lst = client.get("/api/alerts").json()["alerts"]
    assert any(a["fingerprint"] == "abc123" for a in lst)


def test_ack_alert():
    payload = {"alerts": [{"labels": {"alertname": "OOM"}, "annotations": {}, "fingerprint": "xyz"}]}
    client.post("/api/alerts/webhook", json=payload)
    alert = next(a for a in client.get("/api/alerts").json()["alerts"] if a["fingerprint"] == "xyz")
    assert alert["acked"] is False

    ack = client.post(f"/api/alerts/{alert['id']}/ack")
    assert ack.status_code == 200
    alert2 = next(a for a in client.get("/api/alerts").json()["alerts"] if a["id"] == alert["id"])
    assert alert2["acked"] is True


def test_ack_unknown_returns_404():
    assert client.post("/api/alerts/nope/ack").status_code == 404
