"""数据访问层：把「怎么查」集中在这里，路由层只负责编排。

性能要点：
- 学生列表用 LEFT JOIN 一次取出平均分，避免「查学生 + 逐个查成绩」的 N+1 问题。
- 学生成绩用 selectinload 预加载成绩和课程，避免逐条懒加载。
- 分页用 offset/limit，限制 limit 上限防止一次拉全表。
"""
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from . import models


def list_students(db: Session, clazz: str | None = None, skip: int = 0, limit: int = 20):
    q = (
        select(models.Student, func.avg(models.Score.value).label("avg"))
        .outerjoin(models.Score, models.Score.student_id == models.Student.id)
        .group_by(models.Student.id)
        .order_by(models.Student.student_no)
    )
    if clazz:
        q = q.where(models.Student.clazz == clazz)
    rows = db.execute(q.offset(skip).limit(limit)).all()
    return [
        {
            "student_no": s.student_no,
            "name": s.name,
            "clazz": s.clazz,
            "avg": round(avg or 0, 2),
        }
        for s, avg in rows
    ]


def get_student_scores(db: Session, student_no: str):
    return db.execute(
        select(models.Student)
        .options(selectinload(models.Student.scores).selectinload(models.Score.course))
        .where(models.Student.student_no == student_no)
    ).scalar_one_or_none()


def class_stats(db: Session):
    q = (
        select(
            models.Student.clazz,
            func.count(func.distinct(models.Student.id)).label("total"),
            func.avg(models.Score.value).label("avg"),
        )
        .outerjoin(models.Score, models.Score.student_id == models.Student.id)
        .group_by(models.Student.clazz)
        .order_by(models.Student.clazz)
    )
    rows = db.execute(q).all()
    return [{"clazz": c, "total": t, "avg": round(a or 0, 2)} for c, t, a in rows]
