# -*- coding: utf-8 -*-
"""Question controller module"""

from json import loads
from json.decoder import JSONDecodeError

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from tg import expose, abort, request
from tg.controllers.restcontroller import RestController

from ave.model import DBSession, Post
from ave.decorators import authorize


class PostController(RestController):

    @expose('json')
    @authorize
    def get_one(self, post_id):
        """
        Getting a post

        :param post_id :type: int

        :return HttpStatus
        """
        try:
            _id = int(post_id)
        except ValueError:
            abort(status_code=400, detail='post_id must be int', passthrough='json')
        try:
            post = DBSession.query(Post).filter(Post.id == _id).one()
        except NoResultFound:
            abort(status_code=404, detail='No such post', passthrough='json')

        return dict(
            id=post.id,
            parent_id=post.parent_id,
            title=post.title,
            description=post.description,
            creation_date=post.creation_date,
            edit_date=post.edit_date,
            post_type_id=post.post_type_id,
            username=post.account.username,
            account_id=post.account.id,
            votes=post.votes if post.post_type_id == 1 else None,
            views=post.views if post.post_type_id == 1 else None,
            tags=post.tags if post.post_type_id == 1 else None
        )

    @expose('json')
    @authorize
    def get_questions(self, **kw):
        """
        Getting the questions between a range

        :param kw: :type: dict
            {
                'from': value :type: str
                'to': value :type: str
            }

        :return: Json resp containing a list of questions
        """
        if sorted(list(kw.keys())) != sorted(['from', 'to']):
            abort(status_code=400, detail='required keys are not provided', passthrough='json')
        try:
            _from = int(kw['from'])
            to = int(kw['to'])
        except ValueError:
            abort(status_code=400, detail='`from` and `to` must be int', passthrough='json')
        questions = DBSession.query(Post).filter(Post.post_type_id == 1)[_from:to]
        return dict(questions=questions)

    @expose('json')
    @authorize
    def post(self):
        """

        Adding new post

        Getting parameters from tg.request.json
        :param request.json :type: dict
            {
                'title': value :type: str
                'post_type_id': value :type: int
                'parent_id' value :type: int None if post_type_id == 1
                'description': value :type: str
                'account_id': value :type: str
                'tags': value :type: str None if post_type_id != 1
            }

        :return HttpStatus
        """
        required_params = ['post_type_id', 'account_id', 'description', 'parent_id']
        try:
            params = request.json
            if not isinstance(params, dict):
                raise ValueError
        except (JSONDecodeError, ValueError):
            abort(status_code=400, detail='Request is not in Json format', passthrough='json')
        if params['post_type_id'] == 1:
            required_params.append('title')
            required_params.append('tags')
        if sorted(list(params.keys())) != sorted(required_params):
            abort(400, detail='Required keys are not provided', passthrough='json')
        post = Post()
        for k, v in params.items():
            setattr(post, k, v)
        DBSession.add(post)
        try:
            DBSession.flush()
        except IntegrityError:
            abort(400, detail='Post already exists', passthrough='json')
        return dict(id=post.id)

    @expose('json')
    @authorize
    def delete(self, post_id):
        """
        Delete a post

        :param post_id :type: str

        :return: HttpStatus
        """
        try:
            _id = int(post_id)
        except ValueError:
            abort(status_code=400, detail='post_id must be int', passthrough='json')
        try:
            post = DBSession.query(Post).filter(Post.id == _id).one()
            DBSession.delete(post)
        except NoResultFound:
            abort(status_code=404, detail='No such post', passthrough='json')

