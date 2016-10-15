# -*- coding: utf-8 -*-
"""Account controller module"""
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from tg import expose
from tg.exceptions import HTTPBadRequest, HTTPOk, HTTPNotFound
from tg.controllers.restcontroller import RestController

from ave.model import DBSession, Account


class AccountController(RestController):

    @expose('json')
    def get_one(self, account_id):
        """
        Get an account

        :param account_id :type: int

        :return Account :type: dict
        """
        if not isinstance(account_id, int):
            raise HTTPBadRequest(explanation='account_id must be int, rather %s is provided' % type(account_id))
        try:
            account = DBSession.query(Account).filter(Account.id == account_id).one()
        except NoResultFound:
            raise HTTPNotFound()
        return dict(
            username=account.username,
            reputation=account.reputation,
            badges=account.badges,
            created=account.created,
            bio=account.bio
        )

    @expose('json')
    def post(self, **kw):
        """
        Adding new account

        :param kw :type: dict
            {
                'username': value
                'password': value (str)
                'email_address': value (str)
                'bio': value (str)
            }

        :return HttpStatus
        """
        account = Account()
        if list(kw.keys()).sort() != ['username', 'password', 'email_address', 'bio'].sort():
            raise HTTPBadRequest(explanation='required keys are not provided')
        for v in list(kw.values()):
            if not isinstance(v, str):
                raise HTTPBadRequest(explanation='Values must be string. Detected %s with type %s' % (v, type(v)))
        for k, v in kw.items():
            setattr(account, k, v)
        DBSession.add(account)
        try:
            DBSession.flush()
        except IntegrityError:
            raise HTTPBadRequest(explanation='Username or email address is already taken')
        return HTTPOk


