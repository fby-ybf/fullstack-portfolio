package com.fby.score.controller;

import com.fby.score.entity.Course;
import com.fby.score.repository.CourseRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/courses")
@RequiredArgsConstructor
public class CourseController {

    private final CourseRepository courseRepository;

    @GetMapping
    public ResponseEntity<List<Course>> list() {
        return ResponseEntity.ok(courseRepository.findAll());
    }
}
