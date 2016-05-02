from datetime import datetime
from collections import OrderedDict

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime

class Base(object):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    # def extract column data
    # def extract orm data if loaded eager?
    # and...
    def toDict(self): # try to match JSON API
        # TODO: use inspect
        return dict(
            type = self.__tablename__,
            id = self.id,
            attributes = OrderedDict([
                (c.name, getattr(self, c.name))
                for c in self.__mapper__.c if c.name not in ['id']
            ]),
            relationships = OrderedDict([ #can make infinite relationship
                (rel, getattr(self, rel))
                for rel in self.__mapper__.relationships.keys()
            ])
        )

SQLite3Base = declarative_base(cls=Base)
