from sqlalchemy.orm import Mapped
from app.models.base import Base

class CategoryOrm(Base):
    __tablename__ = 'categories'
    name: Mapped[str]