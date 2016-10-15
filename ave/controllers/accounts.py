# -*- coding: utf-8 -*-
"""Account controller module"""
from sqlalchemy.exc import IntegrityError
from tg import expose
from tg.exceptions import HTTPBadRequest, HTTPOk
from tg.controllers.restcontroller import RestController

from ave.model import DBSession, Account


class AccountsController(RestController):

    @expose('json')
    def new(self, **kw):
        """
        Adding new account

        :param kw:
            {
                'username': value
                'password': value
                'email_address': value
                'bio': value
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


