package com.fby.score.controller;

import com.fby.score.dto.ScoreView;
import com.fby.score.service.ScoreService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/scores")
@RequiredArgsConstructor
public class ScoreController {

    private final ScoreService scoreService;

    /** 分页 + 可选过滤（studentId / courseId）查询成绩视图 */
    @GetMapping
    public ResponseEntity<Page<ScoreView>> search(
            @RequestParam(required = false) Long studentId,
            @RequestParam(required = false) Long courseId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        Page<ScoreView> result = scoreService.search(studentId, courseId,
                PageRequest.of(page, size));
        return ResponseEntity.ok(result);
    }

    /** 某学生全部成绩（用于明细页） */
    @GetMapping("/student/{studentId}")
    public ResponseEntity<java.util.List<ScoreView>> byStudent(@PathVariable Long studentId) {
        return ResponseEntity.ok(scoreService.listByStudent(studentId));
    }
}
