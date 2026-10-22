# 付博扬 · 全栈 / 后端开发作品集

> 求职方向：Java 后端 / 全栈开发助理工程师（2027 届 · 榆林大学 人工智能 本科）
> 单仓库 `fullstack-portfolio`，覆盖**后端、数据库、AI 应用、可观测运维**四条主线。

本仓库包含两部分：
1. **`index.html`** —— 在线作品集页面（GitHub Pages 自动部署）。
2. **三个完整代码项目** + **一个企业交付项目介绍（源码不开源）**。

在线地址：`https://fby-ybf.github.io/fullstack-portfolio`

---

## 🏢 MaxKB4j（企业交付项目 · 源码不开源）
> ⚠️ 这是真实企业交付项目，**源码不公开**（涉及交付协议与敏感信息），此处仅做能力展示。
> 技术栈：**SpringBoot 3 · Java 21 · LangChain4j · MySQL · Docker**
> 定位：基于 RAG 的企业知识库问答系统，封装 MaxKB 能力，提供知识库管理、文档解析、向量检索与智能问答网关。
> - 负责范围：知识库检索链路、Agent 编排网关、与现有业务系统的对接与部署。
> - 部署形态：Docker 容器化交付，配套部署手册与运维文档。
> - 部署手册截图（占位，待补充）：① 知识库管理后台 ② 问答网关调用链路 ③ 容器化部署拓扑。

---

## 📦 完整代码项目索引

| 项目 | 技术栈 | 类型 | 说明 |
|---|---|---|---|
| [学生成绩查询系统](score-query-system) | Java 21 / Spring Boot 3 / JPA / 原生 HTML 前端 | 全栈（Java 后端 + 原生前端） | 三表关联、索引与唯一约束、JOIN FETCH 防 N+1、分页、按学分加权 GPA |
| [EduRAG 课程答疑](edurag-qa-fullstack) | FastAPI / 双路召回(BM25+向量) / Vue3+Element Plus | AI 全栈（Python 后端 + Vue 前端） | RAG 问答、SSE 流式输出、文档管理、会话历史、FAQ 置信度拒答 |
| [可观测性监控栈](monitor-stack) | FastAPI / prometheus-client / Vue3 告警面板 | 部署运维（后端埋点 + 告警面板） | 自身埋点 /metrics、Alertmanager webhook 接收、告警处置面板、Prometheus+Grafana 编排 |

> 说明：以上三个均为**独立编写、可运行、可测试、可讲清设计**的演示项目，用于展示工程能力与编码习惯；
> 部署形态、数据均属演示，不代表真实生产系统。真实交付项目（MaxKB4j）源码未公开，以简历与面试为准。

---

## ⚠️ 能力边界（诚实声明）
- **可独立交付**：Java 后端模块开发、MySQL 库表设计与索引优化、Docker 容器化部署与排障、FastAPI 接口开发、Prometheus/Grafana 监控链路、pytest + CI 回归。
- **了解思路、有实操演示但非生产规模**：RAG 双路召回与向量检索、Spring Boot 工程化、Vue3 前端开发。
- **了解思路、无生产实操**：分库分表、分布式事务（Seata / TCC）、微服务 / Spring Cloud、Redis 进阶、React / TypeScript / Vite / Webpack（仅课程与自学接触）、Kubernetes 生产落地、金融账务与高并发生产系统。
- **未涉及**：金融业务（资金流 / 账户体系 / 风控规则）、高并发生产系统、K8s 生产落地。

> 本仓库所有 demo 项目均为本人学习 / 求职目的的独立实现；企业交付项目（MaxKB4j）源码受交付协议约束未开源，相关介绍仅用于能力展示。

## 🔗 联系
邮箱：1502430239@qq.com　·　GitHub：[@fby-ybf](https://github.com/fby-ybf)
