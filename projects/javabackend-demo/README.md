# Spring Boot 后端分层（演示 Demo）

> **定位声明**：这是一个**独立编写的演示项目**，用于展示 Spring Boot + MyBatis 分层工程能力。
> 它与简历中提到的实际交付项目相互独立，不代表真实系统的源码。
>
> **验证状态**：本机无可用 JDK/Maven，**未在本地编译运行**；代码为标准 Maven 工程，
> 已配置 GitHub Actions CI（JDK 17 + `mvn test`），推送后由 CI 云端编译测试作为验证。

## 这是什么

一个最小可运行的 Spring Boot 后端，展示 Controller / Service / Mapper 三层结构 + MyBatis + H2 内存库。

- **分层**：Controller（路由 + 状态码）→ Service（业务逻辑 + 异常）→ Mapper（SQL）。
- **持久层**：MyBatis 注解式 SQL，连 H2 内存数据库，启动即建表 + 灌数据。
- **测试**：`@SpringBootTest` + MockMvc，3 个用例（列表 / 按 id 查 / 404）。

## 快速运行

```bash
# 需要 JDK 17 + Maven
mvn spring-boot:run
# 打开 http://localhost:8080/api/books
```

跑测试：`mvn test`

## 设计要点（面试可讲）

1. **三层各司其职**：Controller 只做参数接转和状态码，Service 放业务规则和异常，Mapper 只写 SQL，改动隔离、易测试。
2. **404 处理**：Service 抛业务异常，Controller 统一转 `ResponseStatusException`，而不是让空指针往上冒。
3. **下划线转驼峰**：MyBatis 配置 `map-underscore-to-camel-case`，SQL 字段和 Java 属性自动映射。

## 目录结构

```
javabackend-demo/
├── pom.xml
└── src/main/java/com/example/demo/
    ├── DemoApplication.java
    ├── controller/BookController.java
    ├── service/BookService.java
    ├── mapper/BookMapper.java
    └── entity/Book.java
```

## 能力边界（诚实）

- 用 H2 内存库演示，**未做 MySQL 迁移与性能调优**。
- 未实现写接口（POST/PUT/DELETE）、登录鉴权、事务管理、分页。
- MyBatis 用的是注解式 SQL，未用 XML 映射与动态 SQL（`<if>`/`<foreach>`）。
