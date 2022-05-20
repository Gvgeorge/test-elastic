from .rubric_base import RubricBase
from .post_base import PostBase
from typing import List


class Rubric(RubricBase):
    id: int
    posts: List[PostBase]


class RubricCreate(RubricBase):
    pass


class RubricUpdate(RubricBase):
    pass
