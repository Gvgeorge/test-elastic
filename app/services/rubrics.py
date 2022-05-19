from typing import List

import tables
from database import get_session
from fastapi import Depends, HTTPException, status
from models.rubrics import Rubric, RubricCreate, RubricUpdate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from utils import get_or_create


class RubricService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, rubric_id: int) -> tables.Rubric:
        rubric = (
            self.session.query(tables.Rubric).filter_by(
                id=rubric_id).first()
        )
        if not rubric:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return rubric

    def get_list(self) -> List[Rubric]:
        rubrics = self.session.query(tables.Rubric).all()
        return rubrics

    def get(self, rubric_id: int) -> tables.Rubric:
        return self._get(rubric_id)

    def create(self, rubric_data: RubricCreate) -> tables.Rubric:
        rubric = tables.Rubric(**rubric_data.dict())
        try:
            self.session.add(rubric)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
        return rubric

    def create_many(self,
                    rubrics_data: List[RubricCreate]
                    ) -> List[tables.Rubric]:
        rubrics = []
        for rubric_data in rubrics_data:
            rubric = self.create(rubric_data)
            rubrics.append(rubric)
        return rubrics

    def get_by_name(self, rubric_name: str) -> tables.Rubric:
        rubric = (
            self.session.query(tables.Rubric).filter_by(
                name=rubric_name).first()
        )
        return rubric

    def update(self, rubric_id: int,  rubric_data: RubricUpdate
               ) -> tables.Rubric:
        rubric = self._get(rubric_id)
        rubric_data.posts = [get_or_create(
            self.session, tables.Post, text=post.text,
            created_datetime=post.created_datetime)[0]
                        for post in rubric_data.posts]
        for field, value in rubric_data:
            setattr(rubric, field, value)
        self.session.commit()
        return rubric

    def delete(self, rubric_id: int) -> None:
        rubric = self._get(rubric_id)
        self.session.delete(rubric)
        self.session.commit()

    def get_or_create_by_name(self, rubric_name: str) -> tables.Rubric:
        return get_or_create(self.session, tables.Rubric, name=rubric_name)


