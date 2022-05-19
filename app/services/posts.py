from sqlalchemy.orm import Session
from fastapi import status, Depends, HTTPException
from models.posts import PostCreate, Post, PostUpdate
from sqlalchemy.orm.attributes import InstrumentedAttribute
from database import get_session
from typing import List
from utils import get_or_create
import tables


class PostService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def _get(self, post_id: int) -> tables.Post:
        post = (
            self.session.query(tables.Post).filter_by(
                id=post_id).first()
        )
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return post

    async def get_list(self) -> List[Post]:
        posts = self.session.query(tables.Post).all()
        return posts

    async def get_many(self, ids: list, sort_by: InstrumentedAttribute
                       ) -> List[Post]:
        posts = self.session.query(tables.Post).filter(
            tables.Post.id.in_(ids)).order_by(sort_by).all()
        return posts

    async def get(self, post_id: int) -> tables.Post:
        return await self._get(post_id)

    async def create(self, post_data: PostCreate) -> tables.Post:
        post = tables.Post(text=post_data.text,
                           created_datetime=post_data.created_datetime)
        post.rubrics = [get_or_create(
            self.session, tables.Rubric, name=rubric.name)[0]
                        for rubric in post_data.rubrics]
        self.session.add(post)
        self.session.commit()
        return post

    async def create_many(
            self, posts_data: List[PostCreate]
            ) -> List[tables.Post]:
        posts = [await self.create(post_data) for post_data in posts_data]
        self.session.add_all(posts)
        self.session.commit()
        return posts

    async def update(self, post_id: int,  post_data: PostUpdate
                     ) -> tables.Post:
        post = await self._get(post_id)
        post_data.rubrics = [get_or_create(
            self.session, tables.Rubric, name=rubric.name)[0]
                        for rubric in post_data.rubrics]
        for field, value in post_data:
            setattr(post, field, value)
        self.session.commit()
        return post

    async def delete(self, post_id: int) -> None:
        post = await self._get(post_id)
        self.session.delete(post)
        self.session.commit()

