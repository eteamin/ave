# -*- coding: utf-8 -*-
"""Question controller module"""

from sqlalchemy.exc import IntegrityError
from tg import expose, abort
from tg.controllers.restcontroller import RestController

from ave.model import DBSession, Post
from ave.decorators import authorize


class QuestionController(RestController):

    @expose('json')
    @authorize
    def post(self, **kw):
        """
        Adding new question

        :param kw :type: dict
            {
                'title': value :type: str
                'post_type': value :type: str
                'description': value :type: str
                'account_id': value :type: str
            }

        :return HttpStatus
        """
        question = Post()
        if sorted(list(kw.keys())) != sorted(['title', 'post_type', 'account_id', 'description']) \
                or kw['post_type'] == '1':
            abort(400, detail='required keys are not provided', passthrough='json')
        for k, v in kw.items():
            setattr(question, k, v)
        DBSession.add(question)
        try:
            DBSession.flush()
        except IntegrityError:
            abort(400, detail='Question already exists', passthrough='json')
