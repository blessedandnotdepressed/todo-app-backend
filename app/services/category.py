from fastapi import APIRouter
from app.repositories.category import CategoryRepository
from sqlalchemy.orm import Session
from app.schemas.category import CategoryRead, CategoryUpdateOrCreate

class CategoryNotFoundError(Exception):
    pass

class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = CategoryRepository
    def get_categories(self) -> list[CategoryRead]:
        categories = self.repository.get_all()
        return [CategoryRead.model_validate(category) for category in categories]

    def create_category(self,payload: CategoryUpdateOrCreate) -> CategoryRead:
        task = self.repository.create(payload.name)
        self.db.commit()
        return CategoryRead.model_validate(task)

    def update_category(self, category_id: str, payload: CategoryUpdateOrCreate):
        category = self.repository.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError
        category.name = payload.name

        self.db.commit()
        return CategoryRead.model_validate(category)

    def delete(self, category_id: str):
        category = CategoryRepository.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError
        self.repository.delete(category)
        self.db.commit()





