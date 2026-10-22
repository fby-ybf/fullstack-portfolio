package com.fby.score.controller;

import com.fby.score.entity.Student;
import com.fby.score.repository.StudentRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/students")
@RequiredArgsConstructor
public class StudentController {

    private final StudentRepository studentRepository;

    /** 分页 + 关键字（学号/姓名）查询 */
    @GetMapping
    public ResponseEntity<Page<Student>> list(
            @RequestParam(required = false, defaultValue = "") String keyword,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        Pageable pageable = PageRequest.of(page, size);
        Page<Student> result;
        if (keyword == null || keyword.isBlank()) {
            result = studentRepository.findAll(pageable);
        } else {
            result = studentRepository
                    .findByStudentNoContainingIgnoreCaseOrNameContainingIgnoreCase(keyword, keyword, pageable);
        }
        return ResponseEntity.ok(result);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Student> detail(@PathVariable Long id) {
        return ResponseEntity.ok(studentRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("学生不存在: " + id)));
    }
}
