"""配置：全部通过环境变量读取，敏感信息只放 .env（已被 .gitignore 忽略）。

.env.example 给出全部可配置项；本地复制为 .env 填写即可，绝不入库。
"""
import os

# LLM 模式：fake（离线演示，无需密钥）/ openai（接入真实大模型）
LLM_MODE = os.getenv("LLM_MODE", "fake")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# 向量召回模式：local（纯 numpy TF-IDF，零依赖可跑）/ milvus（生产，见 docker-compose）
EMBEDDING_MODE = os.getenv("EMBEDDING_MODE", "local")
MILVUS_HOST = os.getenv("MILVUS_HOST", "")
MILVUS_PORT = int(os.getenv("MILVUS_PORT", "19530"))

# Redis（生产用于会话/缓存，演示用内存即可）
REDIS_URL = os.getenv("REDIS_URL", "")

# FAQ 置信度阈值：检索 Top1 归一化得分低于该值视为"知识库无确切答案"
FAQ_THRESHOLD = float(os.getenv("FAQ_THRESHOLD", "0.85"))

# 服务端口
PORT = int(os.getenv("PORT", "8000"))
