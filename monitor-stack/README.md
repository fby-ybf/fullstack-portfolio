# 可观测性监控栈 · monitor-stack

## ✨ 项目简介
一套**可观测性演示栈**：后端服务用 `prometheus-client` **自身埋点**暴露 `/metrics`；同时作为 **Alertmanager 的 webhook 接收端**，把告警落库供前端面板展示；前端是一块**轻量 Vue 告警面板**（只做"列表 / 标记已处理 / 跳转 Grafana"，**不画图表**——图表交给 Grafana）。配套 Prometheus + Alertmanager + Grafana 一键编排。

> 与另外两个项目区分：本项目的 Vue 面板刻意"极简"，聚焦告警处置流，不重复造图表。

## 🛠️ 技术栈
- **后端**：Python 3.11 · FastAPI · prometheus-client · Uvicorn
- **前端**：Vue 3 · Vite · Element Plus（告警列表 + 处置，无图表）
- **可观测组件**：Prometheus · Alertmanager · Grafana（Docker 编排）
- **测试**：pytest + FastAPI TestClient（webhook 接收 / 列表 / 标记 / metrics）

## 🚀 本地开发启动
> 前置：Python 3.11+

**后端（埋点 + webhook 接收）**：
```bash
cd monitor-stack/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# 验证：curl localhost:8000/metrics   curl localhost:8000/api/health
```

**前端（告警面板）**：
```bash
cd monitor-stack/frontend
npm install && npm run dev      # http://localhost:5174 （Vite 已代理 /api → :8000）
```

## 🐳 Docker 一键启动（含 Prometheus/Alertmanager/Grafana）
```bash
cd monitor-stack
docker compose up --build
# 后端        :8000   前端面板  :8080    Grafana  :3000(admin/admin)  Prometheus :9090
```
触发一条测试告警（模拟 Alertmanager 推送）：
```bash
curl -XPOST localhost:8000/api/alerts/webhook -H 'Content-Type: application/json' -d '{
  "alerts":[{"labels":{"alertname":"HighCpu","severity":"warning","instance":"web-01"},
            "annotations":{"summary":"CPU 使用率过高"},"fingerprint":"test1"}]
}'
```
打开 http://localhost:8080 即可在面板看到这条告警，并可"标记已处理"；点"打开 Grafana"看指标图表。

## 📸 功能截图
> 截图占位，待补充：① 告警面板（级别标签 + 已处理标记）② Grafana 指标图表 ③ Prometheus Targets 健康页。

## ⚠️ 局限 & 能力边界
- 告警存储为**内存**，重启丢失；生产应换 Redis / 数据库。本机**未独立部署过 K8s 上的 Prometheus Operator**。
- 面板**不画图表**（按设计交由 Grafana），仅做告警处置流。
- 演示指标为后端自身埋点；生产需补充业务指标与 Node Exporter 等 exporter。
- 已掌握 Prometheus 抓取、Alertmanager 路由与 webhook 接收、Grafana 看板导入的基本链路。
