# -*- coding: utf-8 -*-
"""
Integration tests for the User Interaction. e.g Logging in.

"""
from __future__ import unicode_literals

from nose.tools import eq_, ok_, assert_raises, assert_equal

from ave import model
from ave.model import DBSession
from ave.tests import TestController
from ave.tests.helpers import keep_keys


class TestUser(TestController):
    """
    Tests for the User Controller.

    """
    application_under_test = 'main'

    def test_user(self):
        """Logging in"""

        # Posting an account for login purposes
        valid_account = {
            'username': 'test',
            'password': 'test',
            'email_address': 'test@test.com',
            'bio': 'tester'
        }
        self.app.post('/accounts/', params=valid_account)

        # login to the account posted
        valid_login = {
            'username': 'test',
            'password': 'test'
        }
        login_resp = self.app.post('/users/login', params=valid_login).json
        eq_(
            keep_keys(['username', 'bio'], valid_account),
            keep_keys(['username', 'bio'], login_resp)
        )

        """Going BlackBox"""
        # Invalid username
        invalid_username = {
            'username': 'invalid',
            'password': 'test'
        }
        self.app.post('/users/login', params=invalid_username, status=404)

        # Invalid password
        # TODO: wow!
        # invalid_password = {
        #     'username': 'test',
        #     'password': 'invalid'
        # }
        # self.app.post('/users/login', params=invalid_password, status=401)

        # Invalid request params
        invalid_login = {
            'username': 'test'
        }
        self.app.post('/users/login', params=invalid_login, status=400)

        invalid_login2 = {
            'userrname': 'test',
            'password': 'test'
        }
        self.app.post('/users/login', params=invalid_login2, status=400)
