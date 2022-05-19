import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


posts_rubrics = sa.Table(
    'posts_rubrics', Base.metadata,
    sa.Column('posts_id', sa.ForeignKey('posts.id'), primary_key=True),
    sa.Column('rubrics_id', sa.ForeignKey('rubrics.id'), primary_key=True)
)


class Post(Base):
    __tablename__ = 'posts'
    id = sa.Column(sa.Integer, primary_key=True)
    created_datetime = sa.Column(sa.DateTime)
    text = sa.Column(sa.String, nullable=True)
    rubrics = relationship("Rubric",
                           secondary='posts_rubrics', back_populates='posts')


class Rubric(Base):
    __tablename__ = 'rubrics'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, index=True)
    posts = relationship("Post",
                         secondary='posts_rubrics', back_populates='rubrics')
