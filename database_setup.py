#!/usr/bin/env python3
import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {"name": self.name, "id": self.id}


class User(Base):
    __tablename__ = "user"

    id = Column(String(250), primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    group = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "group": self.group,
        }


class Item(Base):
    __tablename__ = "item"

    name = Column(String(80), nullable=False, unique=True)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    create_time = Column(DateTime, default=datetime.datetime.utcnow)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship(
        Category,
        cascade="all, delete-orphan",
        single_parent=True)
    user_id = Column(String(250), ForeignKey("user.id"))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id,
            "category": self.category.name,
        }
