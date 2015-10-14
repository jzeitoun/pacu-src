from collections import OrderedDict

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base

class Base(object):
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}
    # @declared_attr
    # def __tablename__(cls):
    #     return cls.__name__.lower()
    # id =  Column(Integer, primary_key=True)
    # created_at = Column(DateTime, default=datetime.utcnow)
    def serialize(self, type, normalizer=str):
        attributes = OrderedDict([
            (c.name, normalizer(getattr(self, c.name)))
            for c in self.__mapper__.c if c.name not in ['id']
        ])
        return dict(
            type = type,
            id = self.id,
            attributes = attributes
        )

Base = declarative_base(cls=Base)
