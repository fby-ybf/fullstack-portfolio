"""初始化少量演示数据，方便启动后立刻看到接口返回。

只在表为空时插入，避免每次启动重复造数据。
"""
from . import models
from .database import Base, SessionLocal, engine


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(models.Student).count() > 0:
            return
        s1 = models.Student(student_no="20230001", name="张三", clazz="计科2301")
        s2 = models.Student(student_no="20230002", name="李四", clazz="计科2301")
        s3 = models.Student(student_no="20230003", name="王五", clazz="软件2301")
        c1 = models.Course(course_no="CS101", name="数据结构", credit=4.0)
        c2 = models.Course(course_no="CS102", name="数据库原理", credit=3.0)
        db.add_all([s1, s2, s3, c1, c2])
        db.flush()
        db.add_all(
            [
                models.Score(student_id=s1.id, course_id=c1.id, value=88, status="正常"),
                models.Score(student_id=s1.id, course_id=c2.id, value=92, status="正常"),
                models.Score(student_id=s2.id, course_id=c1.id, value=75, status="正常"),
                models.Score(student_id=s3.id, course_id=c1.id, value=0, status="缺考"),
            ]
        )
        db.commit()
    finally:
        db.close()
