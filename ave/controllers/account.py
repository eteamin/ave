# -*- coding: utf-8 -*-
"""Account controller module"""
from json.decoder import JSONDecodeError

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from tg import expose, abort, request
from tg.controllers.restcontroller import RestController

from ave.model import DBSession, Account
from ave.decorators import authorize


class AccountController(RestController):

    @expose('json')
    @authorize
    def get_one(self, account_id):
        """
        Get an account

        :param account_id :type: str

        :return Account :type: dict
        """
        try:
            _id = int(account_id)
        except ValueError:
            abort(status_code=400, detail='account_id must be int', passthrough='json')
        try:
            account = DBSession.query(Account).filter(Account.id == _id).one()
        except NoResultFound:
            abort(status_code=404, detail='No such user', passthrough='json')
        return dict(
            id=account.id,
            username=account.username,
            reputation=account.reputation,
            badges=account.badges,
            created=account.created,
            bio=account.bio
        )

    @expose('json')
    @authorize
    def post(self):
        """
        Adding new account

        Getting parameters from tg.request.json
        :param request.json :type: dict
            {
                'username': value :type: str
                'password': value :type: str
                'email_address': value :type: str
                'bio': value :type: str
            }

        :return HttpStatus
        """
        try:
            params = request.json
            if not isinstance(params, dict):
                raise ValueError
        except (JSONDecodeError, ValueError):
            abort(status_code=400, detail='Request is not in Json format', passthrough='json')

        account = Account()
        if sorted(list(params.keys())) != sorted(['username', 'password', 'email_address', 'bio']):
            abort(status_code=400, detail='required keys are not provided', passthrough='json')
        for k, v in params.items():
            setattr(account, k, v)
        DBSession.add(account)
        try:
            DBSession.flush()
        except IntegrityError:
            abort(status_code=400, detail='Username or email address is already taken', passthrough='json')
        return dict(
            id=account.id,
            username=account.username,
            reputation=account.reputation,
            badges=account.badges,
            created=account.created,
            bio=account.bio
        )

    @expose('json')
    @authorize
    def delete(self, account_id):
        """
        Delete an Account

        :param account_id :type: str

        :return: HttpStatus
        """
        try:
            _id = int(account_id)
        except ValueError:
            abort(status_code=400, detail='account_id must be int', passthrough='json')
        try:
            account = DBSession.query(Account).filter(Account.id == _id).one()
            DBSession.delete(account)
        except NoResultFound:
            abort(status_code=404, detail='No such user', passthrough='json')
