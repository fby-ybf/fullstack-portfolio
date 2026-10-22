"""FastAPI 入口：路由 + 静态前端 + 依赖注入。"""
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import Base, SessionLocal, engine
from .seed import seed

Base.metadata.create_all(bind=engine)
seed()

app = FastAPI(title="学生成绩查询系统（演示）", version="0.1.0")

# 允许前端页面跨域调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/students", response_model=list[schemas.StudentBrief])
def list_students(
    clazz: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.list_students(db, clazz=clazz, skip=skip, limit=limit)


@app.get("/api/students/{student_no}/scores", response_model=schemas.StudentScores)
def student_scores(student_no: str, db: Session = Depends(get_db)):
    st = crud.get_student_scores(db, student_no)
    if st is None:
        raise HTTPException(status_code=404, detail="学号不存在")
    return {
        "student_no": st.student_no,
        "name": st.name,
        "clazz": st.clazz,
        "scores": [
            {
                "course_no": sc.course.course_no,
                "course_name": sc.course.name,
                "credit": sc.course.credit,
                "value": sc.value,
                "status": sc.status,
            }
            for sc in st.scores
        ],
    }


@app.get("/api/stats/classes", response_model=list[schemas.ClassStat])
def class_stats(db: Session = Depends(get_db)):
    return crud.class_stats(db)


# 静态文件最后挂载，避免吞掉 /api 路由
app.mount("/", StaticFiles(directory="static", html=True), name="static")
