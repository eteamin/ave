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
    username = Column(Unicode(25), unique=True)
    _password = Column('password', Unicode(128))
    email_address = Column(Unicode(50), unique=True)
    bio = Column(Unicode(1000), nullable=True)
    reputation = Column(Integer, default=0)
    badges = Column(Unicode(1000), default='')
    created = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return '<Account: name=%s, email=%s' % (
            repr(self.username),
            repr(self.email_address)
        )

    def __unicode__(self):
        return self.username

    @classmethod
    def _hash_password(cls, password):
        salt = sha256()
        salt.update(os.urandom(60))
        salt = salt.hexdigest()

        hash = sha256()
        # Make sure password is a str because we cannot hash unicode objects
        hash.update((password + salt).encode('utf-8'))
        hash = hash.hexdigest()

        password = salt + hash

        return password

    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        self._password = self._hash_password(password)

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))

    def validate_password(self, password):
        """
        Check the password against existing credentials.

        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool

        """
        hash = sha256()
        hash.update((password + self.password[:64]).encode('utf-8'))
        return self.password[64:] == hash.hexdigest()
