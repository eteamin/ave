# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy.types import Integer
from sqlalchemy.orm import relationship, backref

from ave.model import DeclarativeBase


class Vote(DeclarativeBase):
    """
    Created on Oct, 14, 2016

    Vote for Question, Answer and Comment

    There's a `Value` column indicating `UpVote` or `DownVote`; 1 for `UpVote`, -1 for `DownVote`
    Using a UniqueConstraint to prevent multiple same insertions; e.g. UpVoting multiple times thus
    in case of consecutive UpVoting and DownVoting, only `value` is overwritten.

    """
    __tablename__ = 'votes'

    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)

    account_id = Column(Integer, ForeignKey(
        'accounts.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    account = relationship('Account', backref=backref('votes'))

    post_id = Column(Integer, ForeignKey(
        'posts.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    post = relationship('Post', backref=backref('votes'))

    __table_args__ = (UniqueConstraint('account_id', 'post_id'), )
