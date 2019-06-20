from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, BIGINT
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from models.base_model import BaseModel

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(BIGINT, primary_key=True, nullable=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return str(self.serialize)


class UserModel(BaseModel):
    def all(self):
        users = self.db_session.query(User).all()
        return [user.serialize for user in users]

    def find(self, user_id: int):
        user = self.db_session.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        return user.serialize

    def find_by_email(self, email: str):
        user = self.db_session.query(User).filter(User.email == email).first()
        if not user:
            return None
        return user.serialize

    def create(self, username: str, email: str, password: str):
        hashed_password = self.hash_password(password)
        user = User(username=username, email=email, password=hashed_password)
        self.db_session.add(user)
        self.db_session.commit()
        return user.serialize

    def edit(self, user_id: int, username: str, email: str):
        self.db_session.query(User).filter(User.id == user_id).update({
            'username': username,
            'email': email,
            'updated_at': datetime.now()
        })
        self.db_session.commit()
        return self.find(user_id)

    def delete(self, user_id: int):
        user = self.db_session.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        self.db_session.delete(user)
        self.db_session.commit()
        return user.serialize

    @staticmethod
    def hash_password(password: str):
        return pwd_context.encrypt(password)

    @staticmethod
    def verify_password(password: str, password_hash):
        return pwd_context.verify(password, password_hash)
