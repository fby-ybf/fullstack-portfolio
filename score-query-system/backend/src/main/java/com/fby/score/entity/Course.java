package com.fby.score.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

/**
 * 课程表：演示“一”方实体，credit 用于 GPA 加权。
 */
@Getter
@Setter
@Entity
@Table(name = "course")
public class Course {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "course_code", nullable = false, unique = true, length = 32)
    private String courseCode;

    @Column(name = "course_name", nullable = false, length = 128)
    private String courseName;

    /** 学分 */
    @Column(nullable = false)
    private Double credit;
}
