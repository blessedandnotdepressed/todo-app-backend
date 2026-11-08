from http.client import HTTPException

from starlette.status import HTTP_201_CREATED

from app.api.dependencies import get_category_service
from app.services.category import CategoryService, CategoryNotFoundError
from app.schemas.category import CategoryUpdateOrCreate, CategoryRead
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix='/categories', tags= ['categpries'])

@router.get('', response_model = list[CategoryRead])
def get_categories(service: CategoryService = Depends(get_category_service())) -> list[CategoryRead]:
    return service.get_categories()

@router.post('', response_model = CategoryRead, status_code = status.HTTP_201_CREATED)
def create_category(payload: CategoryUpdateOrCreate, service: CategoryService = Depends(get_category_service())) -> CategoryRead:
    return service.create_category(payload)

@router.patch('/{category_id}', response_model = CategoryUpdateOrCreate)
def update_category(category_id: str, payload: CategoryUpdateOrCreate, service: CategoryService = Depends(get_category_service())) -> CategoryRead:
    try:
        service.update_category(category_id, payload)
    except CategoryNotFoundError:
        raise HTTPException(status = status.HTTP_404_NOT_FOUND, detail = 'Категория не найдена')

@router.delete('/{category_id}')
def delete_category(category_id: str, service: CategoryService = Depends(get_category_service())) -> None:
    try:
        service.delete(category_id)
    except CategoryNotFoundError:
        raise HTTPException(status = status.HTTP_404_NOT_FOUND, detail = 'Категория не найдена')



