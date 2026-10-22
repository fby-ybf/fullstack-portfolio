-- H2 内存库建表（与 sql/init.sql 的 MySQL 版本保持字段一致）
CREATE TABLE student (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_no  VARCHAR(32)  NOT NULL UNIQUE,
    name        VARCHAR(64)  NOT NULL,
    class_name  VARCHAR(64),
    major       VARCHAR(64)
);

CREATE TABLE course (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(32)  NOT NULL UNIQUE,
    course_name VARCHAR(128) NOT NULL,
    credit      DECIMAL(4,2) NOT NULL
);

CREATE TABLE score (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id  BIGINT       NOT NULL,
    course_id   BIGINT       NOT NULL,
    score       DECIMAL(5,2) NOT NULL,
    exam_type   VARCHAR(16)  NOT NULL,
    semester    VARCHAR(16)  NOT NULL,
    CONSTRAINT fk_score_student FOREIGN KEY (student_id) REFERENCES student(id),
    CONSTRAINT fk_score_course  FOREIGN KEY (course_id)  REFERENCES course(id),
    CONSTRAINT uk_score_stu_course_exam_sem
        UNIQUE (student_id, course_id, exam_type, semester)
);

CREATE INDEX idx_score_student ON score(student_id);
CREATE INDEX idx_score_course  ON score(course_id);
