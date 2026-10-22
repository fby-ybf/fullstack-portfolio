package com.fby.score.repository;

import com.fby.score.dto.ScoreView;
import com.fby.score.entity.Score;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface ScoreRepository extends JpaRepository<Score, Long> {

    /**
     * 单条 JOIN 查询成绩视图（学生 + 课程），避免 N+1。
     * 支持按 studentId / courseId 可选过滤，分页返回。
     */
    @Query(value = """
            select new com.fby.score.dto.ScoreView(
                s.name, s.studentNo, c.courseName, c.courseCode,
                sc.score, c.credit, sc.semester, sc.examType)
            from Score sc
            join sc.student s
            join sc.course c
            where (:studentId is null or sc.student.id = :studentId)
              and (:courseId is null or sc.course.id = :courseId)
            order by s.studentNo, c.courseCode
            """,
            countQuery = """
            select count(sc) from Score sc
            where (:studentId is null or sc.student.id = :studentId)
              and (:courseId is null or sc.course.id = :courseId)
            """)
    Page<ScoreView> search(@Param("studentId") Long studentId,
                           @Param("courseId") Long courseId,
                           Pageable pageable);

    /** 取某学生的全部成绩（用于 GPA / 明细页） */
    @Query("""
            select new com.fby.score.dto.ScoreView(
                s.name, s.studentNo, c.courseName, c.courseCode,
                sc.score, c.credit, sc.semester, sc.examType)
            from Score sc
            join sc.student s
            join sc.course c
            where sc.student.id = :studentId
            order by sc.semester, c.courseCode
            """)
    java.util.List<ScoreView> findByStudentId(@Param("studentId") Long studentId);
}
