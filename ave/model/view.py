# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy.types import Integer
from sqlalchemy.orm import relationship, backref

from ave.model import DeclarativeBase


class View(DeclarativeBase):

    """
    Created on Oct, 14, 2016

    View count of Post (Question); caring about how many times a question is viewed and also
    what accounts have viewed it.
    Using a UniqueConstraint so view is counted per user, not per opening the question.

    """

    __tablename__ = 'views'

    id = Column(Integer, primary_key=True)

    account_id = Column(Integer, ForeignKey(
        'accounts.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    account = relationship('Account', backref=backref('views'))

    post_id = Column(Integer, ForeignKey(
        'posts.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    post = relationship('Post', backref=backref('views'))

    __table_args__ = (UniqueConstraint('account_id', 'post_id'), )
