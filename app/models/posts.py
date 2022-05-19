from typing import List
from .post_base import PostBase
from .rubric_base import RubricBase
from .rubrics import RubricCreate, RubricUpdate


class Post(PostBase):
    id: int
    rubrics: List[RubricBase]


class PostCreate(PostBase):
    rubrics: List[RubricCreate]


class PostUpdate(PostBase):
    rubrics: List[RubricUpdate]
