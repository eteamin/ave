# -*- coding: utf-8 -*-

import os
from datetime import datetime
from hashlib import sha256

from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode, DateTime
from sqlalchemy.orm import synonym

from ave.model import DeclarativeBase


class Account(DeclarativeBase):

    """
    Created on Oct, 14, 2016

    User accounts

    """

    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    username = Column(Unicode(25), unique=True, nullable=False)
    _password = Column('password', Unicode(128), nullable=False)
    email_address = Column(Unicode(50), unique=True, nullable=False)
    bio = Column(Unicode(1000), nullable=True)
    reputation = Column(Integer, default=0)
    badges = Column(Unicode(1000), default='')
    created = Column(DateTime, default=datetime.now)

    @classmethod
    def _hash_password(cls, password):
        salt = sha256()
        salt.update(os.urandom(60))
        salt = salt.hexdigest()
        hash = sha256()
        hash.update((password + salt).encode('utf-8'))
        hash = hash.hexdigest()

        password = salt + hash

        return password

    def _set_password(self, password):
        self._password = self._hash_password(password)

    def _get_password(self):
        return self._password

    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))

    def validate_password(self, password):
        hash = sha256()
        hash.update((password + self.password[:64]).encode('utf-8'))
        return self.password[64:] == hash.hexdigest()
