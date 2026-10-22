# 学生成绩查询系统 · score-query-system

## ✨ 项目简介
一个**完整的全栈演示项目**：Java（Spring Boot 3 + Spring Data JPA）提供 RESTful 成绩查询与统计接口，原生 HTML/CSS/JS 前端调用接口展示学生检索、成绩明细与 GPA / 班级平均分。重点演示**三表关联设计、索引与唯一约束、单 JOIN 避免 N+1、分页与按学分加权 GPA 计算**等工程要点。

数据模型：`student（学生）` — `course（课程）` — `score（成绩）` 多对多关系通过成绩表外键实现；成绩表对 `(student_id, course_id, exam_type, semester)` 建唯一约束，防止同一学生同一门课同一次考试重复录入。

## 🛠️ 技术栈
- **后端**：Java 21 · Spring Boot 3.3 · Spring Data JPA · Spring MVC
- **数据库**：H2（默认，零依赖启动）/ MySQL 8.0（生产部署，见 `sql/init.sql`）
- **前端**：原生 HTML + CSS + JavaScript（Fetch API，无构建工具，刻意区别于另外两个 Vue 项目）
- **测试**：JUnit 5 + Spring MockMvc 接口回归
- **部署**：Maven 打包 / 可选 Docker Compose（MySQL）

## 🚀 本地开发启动
> 前置：JDK 21 + Maven 3.9+

```bash
# 1. 进入后端目录
cd score-query-system/backend

# 2. 直接运行（默认 H2 内存库，schema.sql + data.sql 自动初始化演示数据）
mvn spring-boot:run

# 3. 浏览器打开（前端已由 Maven 打包进 static/，同源访问）
#    http://localhost:8080
```

运行测试：
```bash
mvn test
```

切到 MySQL 部署：
```bash
# 先执行建表：mysql -uroot -p score < ../sql/init.sql
mvn spring-boot:run -Dspring.profiles.active=mysql
```

## 🐳 Docker 一键启动（MySQL 模式，可选）
仓库已提供 `docker-compose.yml`（启动 MySQL 并自动导入 `sql/init.sql`）：
```bash
cd score-query-system
docker compose up -d mysql          # 启动数据库
cd backend && mvn spring-boot:run -Dspring.profiles.active=mysql
```

## 📸 功能截图
> 截图占位，待补充：① 学生检索页（关键字 + 分页）② 学生成绩明细 + GPA ③ 课程与班级平均分列表。

## ⚠️ 局限 & 能力边界
- 演示项目，数据为脚本生成的样例数据，**不代表任何真实教务系统**。
- 认证 / 权限、成绩录入与修改接口未实现（仅查询与统计），如需可补充。
- MySQL 部署脚本与索引已给出，但**未在本机做高并发 / 大数据量压测**。
- 前端为原生实现，未使用前端框架；目的是展示“后端 + 轻量前端”的端到端打通能力。
