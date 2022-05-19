from fastapi import APIRouter, Depends, Response, status
from models.rubrics import Rubric, RubricCreate, RubricUpdate
from typing import List
from services.rubrics import RubricService


router = APIRouter(
    prefix='/rubrics',
    tags=['rubrics']
)


@router.get('/', response_model=List[Rubric])
async def get_rubrics(service: RubricService = Depends()):
    return await service.get_list()


@router.get('/{rubric_id}', response_model=Rubric)
async def get_rubric(
    rubric_id: int,
    service: RubricService = Depends()
):
    return await service.get(rubric_id)


@router.post('/', response_model=Rubric)
async def add_rubric(
    rubric_data: RubricCreate,
    service: RubricService = Depends(),
):
    return await service.create(rubric_data)


@router.put('/{rubric_id}', response_model=Rubric)
async def update_rubric(
    rubric_id: int,
    rubric_data: RubricUpdate,
    service: RubricService = Depends(),
):
    return await service.update(rubric_id, rubric_data)


@router.delete('/{rubric_id}')
async def delete_rubric(
    rubric_id: int,
    service: RubricService = Depends(),
):
    await service.delete(rubric_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
