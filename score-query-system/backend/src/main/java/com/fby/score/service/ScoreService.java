package com.fby.score.service;

import com.fby.score.dto.ScoreView;
import com.fby.score.repository.ScoreRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class ScoreService {

    private final ScoreRepository scoreRepository;

    /** 分页 + 可选过滤查询成绩视图（单 JOIN，无 N+1） */
    @Transactional(readOnly = true)
    public Page<ScoreView> search(Long studentId, Long courseId, Pageable pageable) {
        return scoreRepository.search(studentId, courseId, pageable);
    }

    /** 某学生全部成绩 */
    @Transactional(readOnly = true)
    public java.util.List<ScoreView> listByStudent(Long studentId) {
        return scoreRepository.findByStudentId(studentId);
    }
}
