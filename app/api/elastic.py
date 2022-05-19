from typing import List

from fastapi import APIRouter, Depends, Response, status
from models.posts import Post
from services.elastic import ElasticService


router = APIRouter(
    prefix='/elastic',
    tags=['elastic']
)


@router.get('/')
def get_docs(service: ElasticService = Depends()):
    return service.get_list()


@router.post('/add/{doc_id}')
def add_doc(
    post_id: int,
    service: ElasticService = Depends(),
):
    return service.add_to_index(post_id)


@router.delete('/delete_idx/{service_name}')
def delete_idx(
    service_name: str,
    service: ElasticService = Depends(),
):
    service.delete_index(service_name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete('/delete_doc/{doc_id}')
def delete_doc(
    doc_id: int,
    service: ElasticService = Depends(),
):
    service.delete_doc(doc_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/sync')
def sync_with_db(
    service: ElasticService = Depends(),
):
    return service.sync_with_db()


@router.get('/search/{text}/', response_model=List[Post])
def search(text: str, service: ElasticService = Depends()):
    return service.search(text)

# @router.post('/', response_model=Post)
# def add_post(
#     post_data: PostCreate,
#     service: PostService = Depends(),
# ):
#     return service.create(post_data)
