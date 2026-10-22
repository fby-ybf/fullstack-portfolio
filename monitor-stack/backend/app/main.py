"""可观测性监控栈后端。

职责：
  1) 自身埋点：用 prometheus-client 暴露 /metrics（请求数、在途数、延迟分布）。
  2) 告警接收：作为 Alertmanager 的 webhook 接收端，落库（内存）供前端面板展示。
  3) 面板接口：前端告警面板拉取告警列表、标记已处理、跳转 Grafana。

说明：本服务只做"指标暴露 + 告警接入"，不画图表（图表由 Grafana 承担）。
"""
from fastapi import FastAPI, Request
from fastapi.responses import Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
from starlette.middleware.base import BaseHTTPMiddleware

from .store import store

app = FastAPI(title="Monitor Stack", version="1.0.0")

REQUEST_COUNT = Counter("monitor_requests_total", "请求总数", ["method", "endpoint", "status"])
IN_FLIGHT = Gauge("monitor_requests_in_flight", "在途请求数")
REQUEST_LATENCY = Histogram("monitor_request_latency_seconds", "请求延迟(秒)")


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        IN_FLIGHT.inc()
        method = request.method
        path = request.url.path
        with REQUEST_LATENCY.time():
            response = await call_next(request)
        IN_FLIGHT.dec()
        REQUEST_COUNT.labels(method, path, str(response.status_code)).inc()
        return response


app.add_middleware(MetricsMiddleware)


# ---------- 指标 ----------
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# ---------- 告警接口 ----------
@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/alerts/webhook")
async def alert_webhook(payload: dict):
    created = store.add_from_webhook(payload)
    return {"received": len(created)}


@app.get("/api/alerts")
def list_alerts():
    return {"alerts": store.list()}


@app.post("/api/alerts/{alert_id}/ack")
def ack_alert(alert_id: str):
    if not store.ack(alert_id):
        from fastapi import HTTPException
        raise HTTPException(404, "告警不存在")
    return {"ok": True}
