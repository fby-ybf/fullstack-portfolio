package com.fby.score.repository;

import com.fby.score.entity.Student;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

public interface StudentRepository extends JpaRepository<Student, Long>,
        JpaSpecificationExecutor<Student> {

    org.springframework.data.domain.Page<Student> findByStudentNoContainingIgnoreCaseOrNameContainingIgnoreCase(
            String studentNo, String name, org.springframework.data.domain.Pageable pageable);
}
