import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    created_on = Column(DateTime, nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'title': self.title,
            'created_on': self.created_on,
            'id': self.id,
        }


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    desc = Column(String(250), nullable=True)
    created_on = Column(DateTime, nullable=False)
    cid = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)


class User(Base):
    __tablename__ = 'user'

    user = Column(String(50), primary_key=True)
    password = Column(String(250), nullable=False)


engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)