import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import json
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    created_on = Column(DateTime, nullable=False)
    items = relationship("Item")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        if len(self.items) == 0:
            return {
                'id': self.id,
                'name': self.title
            }
        else:
            return {
                'id': self.id,
                'name': self.title,
                'Item': [a.serialize for a in self.items]
            }

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    desc = Column(String(250), nullable=True)
    created_on = Column(DateTime, nullable=False)
    cid = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'cat_id': self.cid,
            'description': self.desc,
            'id': self.id,
            'title': self.title
        }

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), index=True)
    password = Column(String(64), nullable=False)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)