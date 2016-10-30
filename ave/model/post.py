# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime
from sqlalchemy.orm import relationship, backref

from ave.model import DeclarativeBase


class Post(DeclarativeBase):

    """
    Created on Oct, 14, 2016

    Model for Question, Answer and Comment
    Having title, votes, views and tags as nullable fields as a workaround for handling all three Post types
    in a single class.
    parent_id is used for accessing answers and comments of a question, thus null if post_type == 1 (question)

    """

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, nullable=True)  # null if post type is question

    post_type_id = Column(Integer, ForeignKey(
        'post_types.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    post_type = relationship('PostType', backref=backref('posts'))

    title = Column(Unicode(255), nullable=True)  # Null if post type is answer
    description = Column(Unicode(1000), nullable=False, unique=True)
    creation_date = Column(DateTime, nullable=False, default=datetime.now)
    edit_date = Column(DateTime, nullable=True)
    report_count = Column(Integer, nullable=False, default=0)
    tags = Column(Unicode(255), nullable=True)  # Comma separated
    account_id = Column(Integer, ForeignKey(
        'accounts.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    account = relationship('Account', backref=backref('posts'))

    __table_args__ = (UniqueConstraint('account_id', 'description'), )
