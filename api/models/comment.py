from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, BIGINT, TEXT
from datetime import datetime
from models.base_model import BaseModel
Base = declarative_base()


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(BIGINT, primary_key=True, nullable=True)
    user_id = Column(BIGINT, nullable=False)
    post_id = Column(BIGINT, nullable=False)
    body = Column(TEXT, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'body': self.body,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return str(self.serialize)


class CommentModel(BaseModel):
    def all(self):
        comments = self.db_session.query(Comment).all()
        return [comment.serialize for comment in comments]

    def get_post_comments(self, post_id: int):
        comments = self.db_session.query(Comment).filter(Comment.post_id == post_id).all()
        return [comment.serialize for comment in comments]

    def find(self, comment_id: int):
        comment = self.db_session.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            return None
        return comment.serialize

    def create(self, user_id: int, post_id: int, body: str):
        comment = Comment(user_id=user_id, post_id=post_id, body=body)
        self.db_session.add(comment)
        self.db_session.commit()
        return comment.serialize

    def edit(self, comment_id: int, body: str):
        self.db_session.query(Comment).filter(Comment.id == comment_id).update({
            'body': body,
            'updated_at': datetime.now()
        })
        self.db_session.commit()
        return self.find(comment_id)

    def delete(self, comment_id: int):
        comment = self.db_session.query(Comment).filter(Comment.id == comment_id).first()
        self.db_session.delete(comment)
        self.db_session.commit()
        return comment.serialize
