from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

#Подключение к PostgreSQL через Docker (порт 15432)
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:15432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


#Базовый ORM-класс (общий id для всех таблиц)
class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))


#ORM-модели таблиц в базе данных
class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


class CategoryORM(Base):
    __tablename__ = "categories"

    name: Mapped[str]


#Pydantic-схемы для валидации запросов и ответов
class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool


class TaskCreateSchema(BaseModel):
    title: str


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


class CategorySchema(BaseModel):
    id: str
    name: str


class CategoryCreateOrEditSchema(BaseModel):
    name: str


#Жизненный цикл приложения (автосоздание таблиц при старте)
@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

#Настройка CORS для связи с фронтендом на localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Зависимость для получения сессии БД на каждый запрос
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Вспомогательные функции-переводчики (из ORM в Pydantic) ---
def task_orm_to_model(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(
        id=task_orm.id,
        title=task_orm.title,
        completed=task_orm.completed,
    )


def category_orm_to_model(category_orm: CategoryORM) -> CategorySchema:
    return CategorySchema(
        id=category_orm.id,
        name=category_orm.name,
    )


#ЭНДПОИНТЫ ЗАДАЧ (TASKS)

@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    stmt = select(TaskORM)
    tasks_from_db = db.scalars(stmt).all()
    return [task_orm_to_model(task) for task in tasks_from_db]


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    new_task = TaskORM(title=payload.title, completed=False)
    db.add(new_task)
    db.commit()
    return task_orm_to_model(new_task)


@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    task_for_update = db.get(TaskORM, task_id)
    if not task_for_update:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    if payload.title is not None:
        task_for_update.title = payload.title
    if payload.completed is not None:
        task_for_update.completed = payload.completed

    db.commit()
    return task_orm_to_model(task_for_update)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task_for_delete = db.get(TaskORM, task_id)
    if not task_for_delete:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    db.delete(task_for_delete)
    db.commit()


#ЭНДПОИНТЫ КАТЕГОРИЙ (CATEGORIES)

@app.get("/categories")
def read_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
    stmt = select(CategoryORM)
    categories_from_db = db.scalars(stmt).all()
    return [category_orm_to_model(cat) for cat in categories_from_db]


@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateOrEditSchema, db: Session = Depends(get_db)) -> CategorySchema:
    new_category = CategoryORM(name=payload.name)
    db.add(new_category)
    db.commit()
    return category_orm_to_model(new_category)


@app.patch("/categories/{category_id}")
def update_category(category_id: str, payload: CategoryCreateOrEditSchema,
                    db: Session = Depends(get_db)) -> CategorySchema:
    category_for_update = db.get(CategoryORM, category_id)
    if not category_for_update:
        raise HTTPException(status_code=404, detail="Category not found")

    category_for_update.name = payload.name
    db.commit()
    return category_orm_to_model(category_for_update)


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db: Session = Depends(get_db)):
    category_for_delete = db.get(CategoryORM, category_id)
    if not category_for_delete:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category_for_delete)
    db.commit()



