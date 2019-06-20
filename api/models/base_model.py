import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

CONN_STRING = os.environ['CONN_STRING']
engine = create_engine(CONN_STRING)


class BaseModel:
    db_session = Session(bind=engine)

    def all(self):
        pass

    def find(self, entity_id: int):
        pass

    def create(self, **args):
        pass

    def edit(self, **args):
        pass

    def delete(self, entity_id: int):
        pass

    def __del__(self):
        self.db_session.close()
