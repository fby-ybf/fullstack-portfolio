# 学生成绩查询系统（演示 Demo）

> **定位声明**：这是一个**独立编写的学习/演示项目**，用于展示 FastAPI 工程能力与编码习惯。
> 它与简历中提到的任何实际交付项目**相互独立**，不代表真实交付系统的源码。

## 这是什么

一个前后端一起跑的全栈示例：学生 / 课程 / 成绩三张表，提供学生列表（分页 + 班级筛选）、
成绩明细、班级统计三个接口，配一个纯原生 HTML 查询页。

- 后端：**FastAPI + SQLAlchemy 2.0 + SQLite**（可换 PostgreSQL/MySQL）
- 前端：原生 HTML/CSS/JS（fetch 调接口，无框架）
- 测试：**pytest + TestClient**（6 个用例）
- 部署：Dockerfile + GitHub Actions CI

## 快速运行

```bash
# 1. 装依赖（建议用 venv）
pip install -r requirements.txt

# 2. 启动（在项目根目录运行）
uvicorn app.main:app --reload

# 3. 打开浏览器
http://127.0.0.1:8000          # 前端页面
http://127.0.0.1:8000/docs     # 自动生成的接口文档（Swagger）
```

跑测试：

```bash
pytest -q
```

Docker 运行：

```bash
docker build -t score-api-demo .
docker run -p 8000:8000 score-api-demo
```

## 设计要点（面试可讲）

1. **三表设计**：学生、课程是独立实体，成绩是二者间的关联记录（多对多拆表）；
   学号/课程编号唯一，成绩表用 `(student_id, course_id)` 唯一约束保证「一人一科一成绩」。
2. **索引策略**：班级、课程、成绩值都建了索引，按班级/课程/成绩筛选时走索引而非全表扫描。
3. **避免 N+1**：学生列表用 `LEFT JOIN` 一次算出平均分；成绩明细用 `selectinload` 预加载，
   不逐个学生/逐条成绩地查库。
4. **响应模型隔离**：接口只返回 Pydantic 声明的字段，不直接把 ORM 对象吐给前端。
5. **参数校验**：分页 `limit` 上限 100、`skip>=0`，超出直接返回 422。

## 目录结构

```
score-api-demo/
├── app/
│   ├── main.py        # 路由 + 依赖注入 + 静态挂载
│   ├── database.py    # 引擎 + 会话 + Base
│   ├── models.py      # 三张表的 ORM 模型
│   ├── schemas.py     # 响应模型
│   ├── crud.py        # 数据访问（查询集中在里）
│   └── seed.py        # 演示数据
├── static/index.html  # 前端查询页
├── tests/test_api.py  # 接口测试
├── Dockerfile
└── .github/workflows/ci.yml
```

## 能力边界（诚实）

- 本 demo 用 SQLite 跑通，**未做 PostgreSQL/MySQL 迁移与性能压测**。
- 未实现登录鉴权、成绩写入接口（只做了查询侧）。
- 若面试追问「高并发怎么扛」，如实回答：当前是单体 + 单库，高并发场景只了解思路（读写分离、缓存、分库分表），无生产实践。
