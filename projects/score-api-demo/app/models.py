"""ORM 模型：学生 / 课程 / 成绩 三张表。

设计要点（面试可直接讲）：
- 学生与课程是独立实体，成绩是二者之间的关联记录（多对多拆表）。
- 学号、课程编号建唯一索引，防止同一学生/课程重复录入。
- 成绩表用 (student_id, course_id) 唯一约束，保证「一人一科一成绩」。
- 给班级、课程、成绩值建普通索引：查询班级/课程成绩时走索引，而不是全表扫描。
"""
from sqlalchemy import Column, Float, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_no = Column(String(20), unique=True, index=True, nullable=False)  # 学号
    name = Column(String(50), nullable=False)
    clazz = Column(String(30), index=True)  # 班级，建索引方便按班级筛

    scores = relationship("Score", back_populates="student")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_no = Column(String(20), unique=True, index=True, nullable=False)  # 课程编号
    name = Column(String(80), nullable=False)
    credit = Column(Float, default=0.0)

    scores = relationship("Score", back_populates="course")


class Score(Base):
    __tablename__ = "scores"
    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="uq_student_course"),
        Index("ix_score_course", "course_id"),
        Index("ix_score_value", "value"),
    )

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    value = Column(Float, nullable=False)  # 成绩
    status = Column(String(10), default="正常")  # 正常 / 缺考 / 缓考

    student = relationship("Student", back_populates="scores")
    course = relationship("Course", back_populates="scores")
