#в репозиторий добавляем только работу с бдшкой!!! получение, удаление и т.д.

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import TaskOrm

class TaskRepository:
    def __init(self, db: Session):
        self.db = db

    def get_alL(self):
        return self.db.scalars(select(TaskOrm)).all()

    def get_by_id(self, task_id: str) -> TaskOrm | None:
        return self.db.get(TaskOrm, task_id)

    def create(self, title: str) -> TaskOrm:
        task = TaskOrm(title = title, completed = False)
        self.db.add(task)
        return task

    def delete(self, task: TaskOrm) -> None:
        self.db.delete(task)

