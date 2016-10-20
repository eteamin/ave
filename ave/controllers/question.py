# -*- coding: utf-8 -*-
"""Question controller module"""

from sqlalchemy.exc import IntegrityError
from tg import expose, abort
from tg.controllers.restcontroller import RestController

from ave.model import DBSession, Account
from ave.decorators import authorize


class QuestionController(RestController):

    @expose('json')
    @authorize
    def post(self, **kw):
        """
        Adding new question

        :param kw :type: dict
            {
                'username': value :type: str
                'password': value :type: str
                'email_address': value :type: str
                'bio': value :type: str
            }

        :return HttpStatus
        """
        account = Account()
        if sorted(list(kw.keys())) != sorted(['username', 'password', 'email_address', 'bio']):
            abort(400, detail='required keys are not provided', passthrough='json')
        for k, v in kw.items():
            setattr(account, k, v)
        DBSession.add(account)
        try:
            DBSession.flush()
        except IntegrityError:
            abort(400, detail='Username or email address is already taken', passthrough='json')