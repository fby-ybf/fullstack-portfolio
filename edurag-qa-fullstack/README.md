# EduRAG 课程答疑问答系统 · edurag-qa-fullstack

## ✨ 项目简介
基于 **RAG（检索增强生成）** 的课程答疑助手：用户提问 → 双路召回相关文档片段 → 大模型基于片段生成答案并标注来源。**刻意做了"拒答机制"**：当检索置信度低于阈值时，不编造答案，而是提示补充文档或转人工。前端为 Vue3 + Element Plus，包含**流式对话、文档上传管理、会话历史**三个页面。

> 与成绩系统（原生前端）区分：本项目前端使用 **Vue3 + Vite + Element Plus**，展示现代前端工程能力。

## 🛠️ 技术栈
- **后端**：Python 3.11 · FastAPI · Uvicorn · Pydantic v2
- **检索**：BM25（自建 Okapi）+ 向量召回（numpy TF-IDF 余弦）双路融合；生产可切 Milvus
- **生成**：可插拔 LLM（默认 FakeLLM 离线演示；配置 `LLM_MODE=openai` 接真实模型）
- **前端**：Vue 3 · Vite · Element Plus · Axios（SSE 流式消费）
- **基础设施**：Docker / Docker Compose（前端 nginx + 后端 + Redis）

## 🚀 本地开发启动
> 前置：Python 3.11+ 与 Node 18+

**后端**（零依赖即可跑，FakeLLM 无需密钥）：
```bash
cd edurag-qa-fullstack/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # 按需修改；默认 fake 模式可直接跑
uvicorn app.main:app --reload --port 8000
```

**前端**：
```bash
cd edurag-qa-fullstack/frontend
npm install
npm run dev                   # http://localhost:5173 （Vite 已代理 /api → :8000）
```

## 🐳 Docker 一键启动
```bash
cd edurag-qa-fullstack
docker compose up --build
# 浏览器打开 http://localhost:8080
```

## 📸 功能截图
> 截图占位，待补充：① 流式对话页（追问 + 右侧引用来源 + 置信度标签）② 文档管理页（新增/上传/删除）③ 会话历史页。

## ⚠️ 局限 & 能力边界
- 演示用**本地 TF-IDF 向量召回**，未接入真实句向量模型 / Milvus；生产路径已预留（`EMBEDDING_MODE=milvus`）。
- 默认 `LLM_MODE=fake` 为规则化流式吐字，仅用于跑通链路；接入真实模型需自备 API Key。
- **未做**用户认证、文档权限、向量库持久化（重启重建）。这些在真实业务中需补齐。
- FAQ 阈值 `0.85` 是演示取值，实际应根据召回质量离线调参。

## 🔎 核心设计：双路召回 + 拒答阈值
1. **BM25 召回**：擅长精确术语 / 编号匹配（如"发票""退款"）。
2. **向量召回**：擅长同义改写语义匹配。
3. **融合排序**：两路各自归一化到 [0,1] 后等权融合（各 0.5），得到 Top-K 与置信度。
4. **FAQ 阈值**：Top1 置信度 `< 0.85` → 判定"知识库无确切答案"，触发拒答，避免幻觉。
