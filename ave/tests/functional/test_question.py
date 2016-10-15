# -*- coding: utf-8 -*-
"""
Integration tests for the Question.

"""
from __future__ import unicode_literals

from nose.tools import eq_, ok_

from ave import model
from ave.model import DBSession
from ave.tests import TestController


class TestQuestion(TestController):
    """
    Tests for the Question Controller.

    """
    def setUp(self):
        # Insert a test account
        self.test_account = DBSession.add(model.Account(
            username='test',
            password='test',
            email_address='test@test.com',
            bio='tester'
        ))
        # Insert PostTypes
        [DBSession.add(model.PostType(title=i)) for i in ['question', 'answer', 'comment']]

    application_under_test = 'main'

    def test_post_question(self):
        """Question Posting Test"""
        pass

        # Posting a valid question
        # valid_question = {
            # 'post_type_id': '1',
            # 'title': 'test',
            # 'description': 'testing',
            # 'account_id': self.test_account['id']
        # }
        # resp = self.app.post('/question/new', params=valid_question, status=200)
        # Get the question just posted
        # eq_(resp['id'], self.test_account['id'])
