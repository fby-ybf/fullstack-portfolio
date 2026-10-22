"""可观测性 demo 服务：暴露三类指标，供 Prometheus 抓取。

指标（面试可讲）：
- request_duration_seconds：请求耗时直方图，可算 P95；
- request_count_total：请求计数，按路径与状态码分标签；
- app_up：实例存活，恒为 1（由进程存活保证）。
"""
import random
import time

from fastapi import FastAPI, Request
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, Gauge, generate_latest

app = FastAPI(title="可观测性演示服务", version="0.1.0")

REQUEST_COUNT = Counter(
    "request_count_total", "请求总数", ["method", "path", "status"]
)
REQUEST_DURATION = Histogram(
    "request_duration_seconds", "请求耗时", ["path"],
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
)
APP_UP = Gauge("app_up", "服务存活状态")


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """在每个请求前后记录耗时，并打点计数。"""
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    REQUEST_DURATION.labels(path=request.url.path).observe(elapsed)
    REQUEST_COUNT.labels(
        method=request.method, path=request.url.path, status=response.status_code
    ).inc()
    return response


@app.get("/")
def root():
    APP_UP.set(1)
    return {"msg": "ok"}


@app.get("/slow")
def slow():
    """模拟慢请求，便于观察 P95 与告警。"""
    delay = random.uniform(0.05, 0.6)
    time.sleep(delay)
    return {"msg": "slow", "delay": round(delay, 3)}


@app.get("/error")
def error():
    """模拟偶发错误，便于观察错误率告警。"""
    if random.random() < 0.3:
        return Response(status_code=500, content="simulated error")
    return {"msg": "ok"}


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
