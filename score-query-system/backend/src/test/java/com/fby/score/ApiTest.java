package com.fby.score;

import com.fasterxml.jackson.databind.JsonNode;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * 全栈接口回归：基于 H2 内存库（schema.sql + data.sql 自动初始化），
 * 覆盖学生/课程/成绩分页查询与 GPA、班级平均分统计。
 */
@SpringBootTest
@AutoConfigureMockMvc
class ApiTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void studentsPageable() throws Exception {
        mockMvc.perform(get("/api/students").param("page", "0").param("size", "10"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray())
                .andExpect(jsonPath("$.totalElements").value(3));
    }

    @Test
    void studentKeyword() throws Exception {
        mockMvc.perform(get("/api/students").param("keyword", "张伟"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content[0].name").value("张伟"));
    }

    @Test
    void coursesList() throws Exception {
        mockMvc.perform(get("/api/courses"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(4));
    }

    @Test
    void scoresPageable() throws Exception {
        mockMvc.perform(get("/api/scores").param("page", "0").param("size", "5"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray());
    }

    @Test
    void scoresFilterByStudent() throws Exception {
        mockMvc.perform(get("/api/scores").param("studentId", "1").param("size", "50"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalElements").value(4));
    }

    @Test
    void gpaOfStudent1() throws Exception {
        String body = mockMvc.perform(get("/api/stats/gpa").param("studentId", "1"))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();
        JsonNode node = new com.fasterxml.jackson.databind.ObjectMapper().readTree(body);
        // 张伟：88/92/76/85 → 绩点应在 0~4 之间
        double gpa = node.asDouble();
        org.junit.jupiter.api.Assertions.assertTrue(gpa > 0 && gpa <= 4.0, "GPA 应在 (0,4]");
    }

    @Test
    void classAverageOfCourse1() throws Exception {
        mockMvc.perform(get("/api/stats/class-average").param("courseId", "1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isNumber());
    }
}
