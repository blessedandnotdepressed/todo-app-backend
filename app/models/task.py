from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class TaskOrm(Base):
    __tablename__ = 'tasks'

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default = False)
