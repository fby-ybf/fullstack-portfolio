# 可观测性监控栈（演示 Demo）

> **定位声明**：这是一个**独立编写的演示项目**，展示 Prometheus + Grafana 的监控思路。
> 它与简历中提到的实际项目相互独立，不代表真实系统的源码。

## 这是什么

一个最小可运行的监控栈：一个埋了指标的 FastAPI 服务 + Prometheus 抓取 + Grafana 看板。

- 指标：请求耗时直方图、请求计数（按路径/状态码）、实例存活。
- 告警：错误率 > 25%、P95 > 500ms、实例下线三条规则。
- 一键起栈：`docker compose up`。

## 快速运行

```bash
# 方式一：只跑服务（不依赖 Docker）
pip install -r requirements.txt
uvicorn app:app --reload
# http://127.0.0.1:8000/metrics 看指标
# http://127.0.0.1:8000/slow 模拟慢请求
# http://127.0.0.1:8000/error 模拟错误

# 方式二：整栈（需 Docker）
docker compose up
# 服务 8000 / Prometheus 9090 / Grafana 3000
```

## 设计要点（面试可讲）

1. **Histogram 算 P95**：耗时用直方图分桶，`histogram_quantile(0.95, ...)` 可算 P95，比平均值更能反映长尾。
2. **标签设计**：计数按 method/path/status 分标签，能按维度聚合出错误率。
3. **告警要验证**：三条规则覆盖错误率、延迟、存活三类，实践中要「人为制造异常确认告警真的会响」，而不是只写规则。
4. **/metrics 独立暴露**：业务服务只负责埋点打点，Prometheus 主动抓取，服务之间解耦。

## 目录结构

```
monitor-demo/
├── app.py             # 埋点服务 + /metrics
├── prometheus.yml     # 抓取配置
├── alerts.yml         # 告警规则
├── docker-compose.yml # 服务 + Prometheus + Grafana
└── Dockerfile
```

## 能力边界（诚实）

- 未配置 Grafana 看板 JSON（需手动在 3000 端口建面板，或后续补 provisioning）。
- 告警只配置了规则，未接 Alertmanager（告警通知到人）。
- 未做日志采集（如 Loki / ELK），只覆盖了指标（metrics）这一层。
