# -*- coding: utf-8 -*-
"""Login controller"""
from json.decoder import JSONDecodeError

from sqlalchemy.orm.exc import NoResultFound
from tg import abort, expose, request
from tg.controllers.restcontroller import RestController

from ave.model import DBSession, Account
from ave.decorators import authorize

__all__ = ['UserController']


class UserController(RestController):

    @expose('json')
    @authorize
    def login(self):
        """
        Logging into account
        Getting parameters from tg.request.json
        :param request.json :type: dict
            {
                'username': value :type: str
                'password': value :type: str
            }

        :return Account :type: dict or HttpStatus
        """
        try:
            params = request.json
            if not isinstance(params, dict):
                raise ValueError
        except (JSONDecodeError, ValueError):
            abort(status_code=400, detail='Request is not in Json format', passthrough='json')

        if sorted(list(params.keys())) != sorted(['username', 'password']):
            abort(status_code=400, detail='required keys are not provided', passthrough='json')
        username = params['username']
        password = params['password']
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

    @expose('json')
    @authorize
    def require_authentication(self, **kwargs):
        # This is a method for testing authorize decorator
        return dict(OK=True)
