package com.fby.score.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

/**
 * 学生表：演示“一”方实体。
 */
@Getter
@Setter
@Entity
@Table(name = "student")
public class Student {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /** 学号，业务唯一 */
    @Column(name = "student_no", nullable = false, unique = true, length = 32)
    private String studentNo;

    @Column(nullable = false, length = 64)
    private String name;

    @Column(name = "class_name", length = 64)
    private String className;

    @Column(length = 64)
    private String major;
}
