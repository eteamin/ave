# -*- coding: utf-8 -*-
"""Question controller module"""

from tg import expose, redirect, validate, flash, url
from tg.controllers.restcontroller import RestController

from ave.lib.base import BaseController
from ave.model import DBSession

count = 0


class QuestionController(BaseController):

    @expose()
    def test(self):
        global count
        count += 1
        print(count)


