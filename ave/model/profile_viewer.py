# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy.types import Integer
from sqlalchemy.orm import relationship, backref

from ave.model import DeclarativeBase


class ProfileViewer(DeclarativeBase):

    """
    Created on Oct, 14, 2016

    View count of Account ; caring about how many times an account is viewed and also
    what accounts have viewed it.
    Using a UniqueConstraint so view is counted per user, not per opening the account page.

    """

    __tablename__ = 'profile_viewers'

    id = Column(Integer, primary_key=True)

    viewer_account_id = Column(Integer, ForeignKey(
        'accounts.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    account = relationship('Account', backref=backref('profile_viewers'))
