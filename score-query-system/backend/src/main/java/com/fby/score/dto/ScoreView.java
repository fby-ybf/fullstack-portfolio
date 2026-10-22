package com.fby.score.dto;

import com.fby.score.entity.Score;
import lombok.AllArgsConstructor;
import lombok.Getter;

import java.math.BigDecimal;

/**
 * 成绩查询视图 DTO。由 Service 层从 Score 实体（已 JOIN FETCH 学生/课程）映射而来，
 * 避免持久层构造表达式在各 Hibernate 版本间的兼容问题。
 */
@Getter
@AllArgsConstructor
public class ScoreView {
    private final String studentName;
    private final String studentNo;
    private final String courseName;
    private final String courseCode;
    private final BigDecimal score;
    private final BigDecimal credit;
    private final String semester;
    private final String examType;

    public static ScoreView from(Score sc) {
        return new ScoreView(
                sc.getStudent().getName(),
                sc.getStudent().getStudentNo(),
                sc.getCourse().getCourseName(),
                sc.getCourse().getCourseCode(),
                sc.getScore(),
                sc.getCourse().getCredit(),
                sc.getSemester(),
                sc.getExamType());
    }
}
