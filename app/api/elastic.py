from typing import List

from fastapi import APIRouter, Depends, Response, status
from models.posts import Post, PostCreate, PostUpdate
from services.elastic import ElasticService


router = APIRouter(
    prefix='/elastic',
    tags=['elastic']
)


@router.get('/')
async def get_docs(service: ElasticService = Depends()):
    return await service.get_list()


@router.post('/add/')
async def add_doc(
    post_data: PostCreate,
    service: ElasticService = Depends(),
):
    return await service.add(post_data)


@router.delete('/delete_idx/{service_name}')
async def delete_idx(
    service_name: str,
    service: ElasticService = Depends(),
):
    await service.delete_index(service_name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete('/delete_doc/{doc_id}')
async def delete_doc(
    doc_id: int,
    service: ElasticService = Depends(),
):
    await service.delete_doc(doc_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/sync')
async def sync_with_db(
    service: ElasticService = Depends(),
):
    return await service.sync_with_db()


@router.get('/search/{text}/', response_model=List[Post])
async def search(text: str, service: ElasticService = Depends()):
    return await service.search(text)


@router.put('/{doc_id}', response_model=Post)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    service: ElasticService = Depends(),
):
    return await service.update(post_id, post_data)
