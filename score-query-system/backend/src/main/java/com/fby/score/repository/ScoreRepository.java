package com.fby.score.repository;

import com.fby.score.entity.Score;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface ScoreRepository extends JpaRepository<Score, Long> {

    /**
     * 单条 JOIN FETCH 同时取出 student / course，避免先查成绩再逐条查学生/课程导致的 N+1。
     * 支持按 studentId / courseId 可选过滤，分页返回实体（在 Service 层映射为视图 DTO）。
     */
    @Query("""
            select sc from Score sc
            join fetch sc.student s
            join fetch sc.course c
            where (:studentId is null or sc.student.id = :studentId)
              and (:courseId is null or sc.course.id = :courseId)
            order by s.studentNo, c.courseCode
            """)
    Page<Score> search(@Param("studentId") Long studentId,
                       @Param("courseId") Long courseId,
                       Pageable pageable);

    /** 某学生的全部成绩（JOIN FETCH 关联，无 N+1） */
    @Query("""
            select sc from Score sc
            join fetch sc.student s
            join fetch sc.course c
            where sc.student.id = :studentId
            order by sc.semester, c.courseCode
            """)
    java.util.List<Score> findByStudentId(@Param("studentId") Long studentId);
}
