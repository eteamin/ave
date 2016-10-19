# -*- coding: utf-8 -*-
"""Login controller"""
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from tg import abort, expose
from ave.lib.base import BaseController
from ave.model import DBSession, Account


__all__ = ['UserController']


class UserController(BaseController):
    @expose('json')
    def login(self, **kw):
        """
        Logging into account

        :param kw :type: dict
            {
                'username': value :type: str
                'password': value :type: str
            }

        :return Account :type: dict or HttpStatus
        """
        if sorted(list(kw.keys())) != sorted(['username', 'password']):
            abort(status_code=400, detail='required keys are not provided', passthrough='json')
        username = kw['username']
        password = kw['password']
        try:
            user = DBSession.query(Account).filter(Account.username == username).one()
        except NoResultFound:
            abort(status_code=400, detail='Invalid username or password', passthrough='json')
        if not user.validate_password(password):
            abort(status_code=401, detail='Invalid password', passthrough='json')
        return dict(
            id=user.id,
            username=user.username,
            reputation=user.reputation,
            badges=user.badges,
            created=user.created,
            bio=user.bio
        )
