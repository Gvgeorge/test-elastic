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

    def _get(self, post_id: int) -> tables.Post:
        post = (
            self.session.query(tables.Post).filter_by(
                id=post_id).first()
        )
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return post

    def get_list(self) -> List[Post]:
        posts = self.session.query(tables.Post).all()
        return posts

    def get_many(self, ids: list, sort_by: InstrumentedAttribute) -> List[Post]:
        posts = self.session.query(tables.Post).filter(
            tables.Post.id.in_(ids)).order_by(sort_by).all()
        return posts

    def get(self, post_id: int) -> tables.Post:
        return self._get(post_id)

    def create(self, post_data: PostCreate) -> tables.Post:
        post = tables.Post(text=post_data.text,
                           created_datetime=post_data.created_datetime)
        post.rubrics = [get_or_create(
            self.session, tables.Rubric, name=rubric.name)[0]
                        for rubric in post_data.rubrics]
        self.session.add(post)
        self.session.commit()
        return post

    def create_many(self,
                    posts_data: List[PostCreate]
                    ) -> List[tables.Post]:
        posts = [self.create(post_data) for post_data in posts_data]
        self.session.add_all(posts)
        self.session.commit()
        return posts

    def update(self, post_id: int,  post_data: PostUpdate
               ) -> tables.Post:
        post = self._get(post_id)
        post_data.rubrics = [get_or_create(
            self.session, tables.Rubric, name=rubric.name)[0]
                        for rubric in post_data.rubrics]
        print('post_data:', post_data)
        for field, value in post_data:
            setattr(post, field, value)
        self.session.commit()
        return post

    def delete(self, post_id: int) -> None:
        post = self._get(post_id)
        self.session.delete(post)
        self.session.commit()

