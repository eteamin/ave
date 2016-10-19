# -*- coding: utf-8 -*-
"""
Integration tests for the Question.

"""
from __future__ import unicode_literals

from nose.tools import eq_, ok_

from ave.tests import TestController


class TestQuestion(TestController):
    """
    Tests for the Question Controller.

    """

    application_under_test = 'main'

    def test_question(self):
        """Question Controller Test"""

        # Posting an account
        account = {
            'username': 'test',
            'password': 'test',
            'email_address': 'test@test.com',
            'bio': 'tester'
        }
        account_post_resp = self.app.post('/accounts/', params=account).json

        # Posting a valid question
        valid_question = {
            'post_type_id': '1',
            'title': 'test',
            'description': 'testing',
            'account_id': account_post_resp['id']
        }
        # resp = self.app.post('/questions/', params=valid_question).json
