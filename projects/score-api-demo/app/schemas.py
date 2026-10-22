"""Pydantic 响应模型：定义 API 返回结构，同时控制哪些字段暴露给前端。

接口层只返回这里声明的字段，不把 ORM 对象直接吐出去，
避免意外泄露内部字段（如主键 id、外键）以及循环引用。
"""
from pydantic import BaseModel


class ScoreOut(BaseModel):
    course_no: str
    course_name: str
    credit: float
    value: float
    status: str

    model_config = {"from_attributes": True}


class StudentScores(BaseModel):
    student_no: str
    name: str
    clazz: str
    scores: list[ScoreOut]


class StudentBrief(BaseModel):
    student_no: str
    name: str
    clazz: str
    avg: float


class ClassStat(BaseModel):
    clazz: str
    total: int
    avg: float
