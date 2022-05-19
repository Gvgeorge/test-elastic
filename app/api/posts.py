from fastapi import APIRouter, Depends, Response, status
from models.posts import PostCreate, Post, PostUpdate
from typing import List, Optional
from services.posts import PostService


router = APIRouter(
    prefix='/posts',
    tags=['posts']
)


@router.get('/', response_model=List[Post])
def get_posts(
    service: PostService = Depends(),
):
    return service.get_list()


@router.get('/{post_id}', response_model=Post)
def get_post(
    post_id: int,
    service: PostService = Depends(),
):
    return service.get(post_id)


@router.post('/', response_model=Post)
def add_post(
    post_data: PostCreate,
    service: PostService = Depends(),
):
    return service.create(post_data)


@router.put('/{post_id}', response_model=Post)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    service: PostService = Depends(),
):
    return service.update(post_id, post_data)


@router.delete('/{post_id}')
def delete_post(
    post_id: int,
    service: PostService = Depends(),
):
    service.delete(post_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
