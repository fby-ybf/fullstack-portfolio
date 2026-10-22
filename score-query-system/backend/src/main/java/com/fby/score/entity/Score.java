package com.fby.score.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;

/**
 * 成绩表：演示“多”方实体。
 * 与 student / course 用 @ManyToOne 关联，便于一次 JOIN 取出视图，避免 N+1。
 * 唯一约束 (student_id, course_id, exam_type, semester) 防止同一学生同一门课同一次考试重复录入。
 */
@Getter
@Setter
@Entity
@Table(name = "score", uniqueConstraints = {
        @UniqueConstraint(name = "uk_score_stu_course_exam_sem",
                columnNames = {"student_id", "course_id", "exam_type", "semester"})
}, indexes = {
        @Index(name = "idx_score_student", columnList = "student_id"),
        @Index(name = "idx_score_course", columnList = "course_id")
})
public class Score {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "student_id", nullable = false)
    private Student student;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "course_id", nullable = false)
    private Course course;

    /** 分数（百分制） */
    @Column(nullable = false, precision = 5, scale = 2)
    private BigDecimal score;

    /** 考试类型：期末 / 期中 / 补考 */
    @Column(name = "exam_type", nullable = false, length = 16)
    private String examType;

    /** 学期，如 2024-2025-1 */
    @Column(nullable = false, length = 16)
    private String semester;
}
