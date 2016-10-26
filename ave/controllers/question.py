# -*- coding: utf-8 -*-
"""Question controller module"""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from tg import expose, abort
from tg.controllers.restcontroller import RestController

from ave.model import DBSession, Post
from ave.decorators import authorize


class QuestionController(RestController):

    @expose('json')
    @authorize
    def get_one(self, question_id):
        """
        Adding new question

        :param question_id :type: int

        :return HttpStatus
        """
        try:
            _id = int(question_id)
        except ValueError:
            abort(status_code=400, detail='question_id must be int', passthrough='json')
        try:
            question = DBSession.query(Post).filter(Post.id == _id).one()
        except NoResultFound:
            abort(status_code=404, detail='No such question', passthrough='json')
        return dict(
            title=question.title,
            description=question.description,
            creation_date=question.creation_date,
            edit_date=question.edit_date,
            post_type_id=question.post_type_id,
            username=question.account.username
        )

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
        if sorted(list(kw.keys())) != sorted(['title', 'post_type_id', 'account_id', 'description']) \
                or kw['post_type_id'] != '1':
            abort(400, detail='required keys are not provided', passthrough='json')
        for k, v in kw.items():
            setattr(question, k, v)
        DBSession.add(question)
        try:
            DBSession.flush()
        except IntegrityError:
            abort(400, detail='Question already exists', passthrough='json')
        return dict(id=question.id)
