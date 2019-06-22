from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, BIGINT, TEXT
from datetime import datetime
from models.base_model import BaseModel

Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    id = Column(BIGINT, primary_key=True, nullable=True)
    user_id = Column(BIGINT, nullable=False)
    title = Column(String(255), nullable=False)
    body = Column(TEXT, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'body': self.body,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return str(self.serialize)


class PostModel(BaseModel):
    def all(self):
        posts = self.db_session.query(Post).all()
        return [post.serialize for post in posts]

    def user_posts(self, user_id: int):
        posts = self.db_session.query(Post).filter(Post.user_id == user_id).all()
        return [post.serialize for post in posts]

    def find(self, post_id: int):
        post = self.db_session.query(Post).filter(Post.id == post_id).first()
        if not post:
            return None
        return post.serialize

    def create(self, user_id: int, title: str, body: str):
        post = Post(user_id=user_id, title=title, body=body)
        self.db_session.add(post)
        self.db_session.commit()
        return post.serialize

    def edit(self, post_id: int, title: str, body: str):
        self.db_session.query(Post).filter(Post.id == post_id).update({
            'title': title,
            'body': body,
            'updated_at': datetime.now()
        })
        self.db_session.commit()
        return self.find(post_id)

    def delete(self, post_id: int):
        post = self.db_session.query(Post).filter(Post.id == post_id).first()
        if not post:
            return None
        self.db_session.delete(post)
        self.db_session.commit()
        return post.serialize
