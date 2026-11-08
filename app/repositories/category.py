from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import CategoryOrm

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.scalars(select(CategoryOrm)).all()

    def get_by_id(self, category_id: str) -> CategoryOrm | None:
        return self.db.get(CategoryOrm,category_id)

    def create(self, name: str) -> CategoryOrm:
        new_category = CategoryOrm(name = name)
        self.db.add(new_category)
        return new_category

    def delete(self,category: CategoryOrm):
        self.db.delete(category)
