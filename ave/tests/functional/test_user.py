# -*- coding: utf-8 -*-
"""
Integration tests for the User Interaction. e.g Logging in.

"""
from nose.tools import eq_, ok_, assert_raises, assert_equal

from ave.tests import TestController
from ave.tests.helpers import keep_keys, make_auth_header


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
        self.app.post_json('/accounts/', params=valid_account, headers=make_auth_header())

        # login to the account posted
        valid_login = {
            'username': 'test',
            'password': 'test'
        }
        login_resp = self.app.post_json('/users/login', params=valid_login, headers=make_auth_header()).json
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
        self.app.post_json('/users/login', params=invalid_username, headers=make_auth_header(),  status=400)

        # Invalid password
        invalid_password = {
            'username': 'test',
            'password': 'invalid'
        }
        self.app.post_json('/users/login', params=invalid_password, headers=make_auth_header(), status=401)

        # Invalid request params
        invalid_login = {
            'username': 'test'
        }
        self.app.post_json('/users/login', params=invalid_login, headers=make_auth_header(), status=400)

        invalid_login2 = {
            'userrname': 'test',
            'password': 'test'
        }
        self.app.post_json('/users/login', params=invalid_login2, headers=make_auth_header(), status=400)

        # Invalid Json format
        self.app.post_json('/users/login', params=[], headers=make_auth_header(), status=400)

