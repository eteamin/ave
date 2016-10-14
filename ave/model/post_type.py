# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode

from ave.model import DeclarativeBase


class PostType(DeclarativeBase):
    """
    Created on Oct, 14, 2016

    Post types are Question, Answer, Comment

    """
    __tablename__ = 'post_types'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(25), nullable=True)
