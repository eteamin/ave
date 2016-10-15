# -*- coding: utf-8 -*-
"""{{target.capitalize()}} controller module"""

from tg import expose, redirect, validate, flash, url
from tg.controllers.restcontroller import RestController

from ave.model import DBSession


class QuestionController(RestController):

    @expose('json')
    def new(self, **kw):
        pass
