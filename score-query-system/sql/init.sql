-- 学生成绩查询系统 · MySQL 部署建表脚本
-- 用法：mysql -uroot -p score < sql/init.sql
-- 注意：MySQL 模式由 schema.sql（H2）对应而来，字段与索引保持一致。

CREATE DATABASE IF NOT EXISTS score
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_general_ci;

USE score;

CREATE TABLE IF NOT EXISTS student (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_no  VARCHAR(32)  NOT NULL,
    name        VARCHAR(64)  NOT NULL,
    class_name  VARCHAR(64)  DEFAULT NULL,
    major       VARCHAR(64)  DEFAULT NULL,
    UNIQUE KEY uk_student_no (student_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS course (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(32)  NOT NULL,
    course_name VARCHAR(128) NOT NULL,
    credit      DECIMAL(4,2) NOT NULL,
    UNIQUE KEY uk_course_code (course_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS score (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id  BIGINT       NOT NULL,
    course_id   BIGINT       NOT NULL,
    score       DECIMAL(5,2) NOT NULL,
    exam_type   VARCHAR(16)  NOT NULL,
    semester    VARCHAR(16)  NOT NULL,
    KEY idx_score_student (student_id),
    KEY idx_score_course (course_id),
    UNIQUE KEY uk_score_stu_course_exam_sem (student_id, course_id, exam_type, semester),
    CONSTRAINT fk_score_student FOREIGN KEY (student_id) REFERENCES student(id),
    CONSTRAINT fk_score_course  FOREIGN KEY (course_id)  REFERENCES course(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
