# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode

from ave.model import DeclarativeBase


class Badge(DeclarativeBase):

    """
    Created on Oct, 14, 2016

    Badges for users,
    Badges are not to be `CRUD`ed by users.

    """

    __tablename__ = 'badges'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(25), nullable=False)
