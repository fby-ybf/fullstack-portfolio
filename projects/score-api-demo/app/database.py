"""数据库连接与会话管理。

开发环境使用 SQLite（零配置、可直接跑）；切到 PostgreSQL/MySQL 只需改
SQLALCHEMY_DATABASE_URL，并去掉 connect_args 里的 SQLite 专用参数。
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# SQLite 示例；生产换成 postgresql://user:pass@host/db 或 mysql+pymysql://...
SQLALCHEMY_DATABASE_URL = "sqlite:///./score.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # SQLite 默认禁止跨线程共享连接，这里打开以免 FastAPI 多请求报错；
    # 换成 PostgreSQL/MySQL 后删除这一行。
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """所有 ORM 模型的基类。"""
