from datetime import datetime
from collections import OrderedDict

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy import inspect

def parallelize(iterable, func):
    for i in iterable:
        yield i, func(i)

class Base(object):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    def toDict(self):
        return self.as_jsonapi
    @property
    def as_jsonapi(self):
        return dict(
            type = self.__tablename__,
            id = self.id,
            attributes = self.attributes,
            relationships = self.relationships)
    @property
    def attributes(self):
        return OrderedDict([
            (c.key, getattr(self, c.key))
        for c in inspect(type(self)).columns])
    @property
    def relationships(self):
        rels = inspect(type(self)).relationships
        return OrderedDict([
            (rel.key, obj if rel.uselist else obj.attributes
            ) for rel, obj in parallelize(rels, lambda r: getattr(self, r.key))
        ])
    @classmethod
    def init_and_update(cls, **kwargs):
        payload = {key: kwargs.pop(key)
            for key in cls.__mapper__.c.keys()
            if key in kwargs}
        self = cls(**payload)
        self.__dict__.update(kwargs)
        return self

SQLite3Base = declarative_base(cls=Base)
