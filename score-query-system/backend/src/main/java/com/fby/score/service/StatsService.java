package com.fby.score.service;

import com.fby.score.dto.ScoreView;
import com.fby.score.repository.ScoreRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;

@Service
@RequiredArgsConstructor
public class StatsService {

    private final ScoreRepository scoreRepository;

    /**
     * 计算学生 GPA（4.0 制，按学分加权）。
     * 同一门课取最高分（期末优先于补考）计入，避免补考低分拉低绩点。
     */
    @Transactional(readOnly = true)
    public BigDecimal computeGpa(Long studentId) {
        List<ScoreView> all = scoreRepository.findByStudentId(studentId);
        if (all.isEmpty()) {
            return BigDecimal.ZERO.setScale(2, RoundingMode.HALF_UP);
        }
        // 同一课程保留最高分
        java.util.Map<String, BigDecimal> best = new java.util.HashMap<>();
        java.util.Map<String, BigDecimal> creditOf = new java.util.HashMap<>();
        for (ScoreView v : all) {
            BigDecimal cur = best.getOrDefault(v.getCourseCode(), BigDecimal.ZERO);
            if (v.getScore().compareTo(cur) > 0) {
                best.put(v.getCourseCode(), v.getScore());
                creditOf.put(v.getCourseCode(), v.getCredit());
            }
        }
        BigDecimal creditSum = BigDecimal.ZERO;
        BigDecimal weighted = BigDecimal.ZERO;
        for (var e : best.entrySet()) {
            BigDecimal credit = creditOf.get(e.getKey());
            creditSum = creditSum.add(credit);
            weighted = weighted.add(toGradePoint(e.getValue()).multiply(credit));
        }
        if (creditSum.compareTo(BigDecimal.ZERO) == 0) {
            return BigDecimal.ZERO.setScale(2, RoundingMode.HALF_UP);
        }
        return weighted.divide(creditSum, 4, RoundingMode.HALF_UP)
                .setScale(2, RoundingMode.HALF_UP);
    }

    /** 某课程的全班平均分（百分制） */
    @Transactional(readOnly = true)
    public BigDecimal classAverage(Long courseId) {
        List<ScoreView> all = scoreRepository.search(null, courseId,
                org.springframework.data.domain.Pageable.unpaged()).getContent();
        if (all.isEmpty()) {
            return BigDecimal.ZERO.setScale(2, RoundingMode.HALF_UP);
        }
        BigDecimal sum = BigDecimal.ZERO;
        for (ScoreView v : all) {
            sum = sum.add(v.getScore());
        }
        return sum.divide(BigDecimal.valueOf(all.size()), 2, RoundingMode.HALF_UP);
    }

    /** 百分制分数 → 4.0 绩点（标准换算） */
    private BigDecimal toGradePoint(BigDecimal score) {
        double s = score.doubleValue();
        if (s >= 90) return BigDecimal.valueOf(4.0);
        if (s >= 85) return BigDecimal.valueOf(3.7);
        if (s >= 82) return BigDecimal.valueOf(3.3);
        if (s >= 78) return BigDecimal.valueOf(3.0);
        if (s >= 75) return BigDecimal.valueOf(2.7);
        if (s >= 72) return BigDecimal.valueOf(2.3);
        if (s >= 68) return BigDecimal.valueOf(2.0);
        if (s >= 64) return BigDecimal.valueOf(1.5);
        if (s >= 60) return BigDecimal.valueOf(1.0);
        return BigDecimal.ZERO;
    }
}
