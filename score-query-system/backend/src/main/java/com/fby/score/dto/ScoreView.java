package com.fby.score.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;

import java.math.BigDecimal;

/**
 * 成绩查询视图 DTO：通过一条 JPQL JOIN 把学生名、课程名、学分、分数一次性取出，
 * 避免先查成绩再逐条查学生/课程导致的 N+1 查询。
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
}
