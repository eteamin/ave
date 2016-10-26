# -*- coding: utf-8 -*-
"""Question controller module"""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from tg import expose, abort
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
            votes=post.votes,
            views=post.views,
            tags=post.tags
        )

    @expose('json')
    @authorize
    def post(self, **kw):
        """
        Adding new post

        :param kw :type: dict
            {
                'title': value :type: str
                'post_type_id': value :type: str
                'parent_id' value :type: str None if post_type_id == 1
                'description': value :type: str
                'account_id': value :type: str
                'tags': value :type: str None if post_type_id != 1
            }

        :return HttpStatus
        """
        post = Post()
        if sorted(
                list(kw.keys())
        ) != sorted(
                ['title',
                 'post_type_id',
                 'account_id',
                 'description',
                 'tags',
                 'parent_id']
        ):
            abort(400, detail='Required keys are not provided', passthrough='json')
        for k, v in kw.items():
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

