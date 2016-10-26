# -*- coding: utf-8 -*-
"""
Integration tests for the Question.

"""

from nose.tools import eq_, assert_equal, assert_dict_equal

from ave.tests import TestController
from ave.tests.helpers import make_auth_header, keep_keys


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
        account_post_resp = self.app.post('/accounts/', params=account, headers=make_auth_header()).json

        # Posting a valid question
        valid_question = {
            'post_type_id': 1,
            'title': 'test',
            'description': 'testing',
            'account_id': account_post_resp['id']
        }
        post_resp = self.app.post('/questions/', params=valid_question, headers=make_auth_header()).json
        
        # Get the question just posted
        get_resp = self.app.get('/questions/%s' % post_resp['id'], headers=make_auth_header()).json
        eq_(
            keep_keys(['post_type_id', 'title', 'description'], get_resp),
            keep_keys(['post_type_id', 'title', 'description'], valid_question)
        )
        assert_equal(account['username'], get_resp['username'])
        # Question dict lacking pairs
        invalid_question = {
            'post_type_id': '1',
            'title': 'test',
            'account_id': account_post_resp['id']
        }
        self.app.post('/questions/', params=invalid_question, headers=make_auth_header(), status=400)

        # Question with invalid key
        invalid_question2 = {
            'post_type_id': '1',
            'invalid_key': 'test',
            'description': 'testing',
            'account_id': account_post_resp['id']
        }
        self.app.post('/questions/', params=invalid_question2, headers=make_auth_header(), status=400)

        # Trying to violate description uniqueness by posting valid_question again
        self.app.post('/questions/', params=valid_question, headers=make_auth_header(), status=400)
