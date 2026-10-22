package com.fby.score.controller;

import com.fby.score.service.StatsService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;

@RestController
@RequestMapping("/api/stats")
@RequiredArgsConstructor
public class StatsController {

    private final StatsService statsService;

    /** 学生 GPA（4.0 制，按学分加权） */
    @GetMapping("/gpa")
    public ResponseEntity<BigDecimal> gpa(@RequestParam Long studentId) {
        return ResponseEntity.ok(statsService.computeGpa(studentId));
    }

    /** 某课程全班平均分 */
    @GetMapping("/class-average")
    public ResponseEntity<BigDecimal> classAverage(@RequestParam Long courseId) {
        return ResponseEntity.ok(statsService.classAverage(courseId));
    }
}
