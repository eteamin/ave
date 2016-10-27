# -*- coding: utf-8 -*-
"""
Integration tests for the Account.

"""
from nose.tools import eq_, assert_equal

from ave.tests import TestController
from ave.tests.helpers import keep_keys, make_auth_header


class TestAccount(TestController):
    """
    Tests for the Account Controller.

    """
    application_under_test = 'main'

    def test_account(self):
        """Account Post, Get Test"""

        """WhiteBox Testing"""

        # Posting a valid account
        valid_account = {
            'username': 'test',
            'password': 'test',
            'email_address': 'test@test.com',
            'bio': 'tester'
        }
        post_resp = self.app.post_json('/accounts/', params=valid_account, headers=make_auth_header()).json

        # Get the account just posted
        get_resp = self.app.get('/accounts/%s' % post_resp['id'], headers=make_auth_header()).json
        eq_(
            keep_keys(['username', 'bio'], valid_account),
            keep_keys(['username', 'bio'], get_resp)
        )
        assert_equal(get_resp['reputation'], 0)
        assert_equal(get_resp['badges'], '')

        # Delete the account just got
        self.app.delete('/accounts/%s' % get_resp['id'], headers=make_auth_header())

        # Get the account just deleted
        self.app.get('/accounts/%s' % get_resp['id'], headers=make_auth_header(), status=404)

        """BlackBox Testing"""

        # Typo in keys
        invalid_account = {
            'username': 'invalid',
            'passwosrd': 'invalid',
            'email_address': 'invalid@test.com',
            'bio': 'invalid tester'
        }
        self.app.post_json('/accounts/', params=invalid_account, headers=make_auth_header(), status=400)

        # Dict lacking one pair
        invalid_account2 = {
            'username': 'invalid',
            'password': 'invalid',
            'bio': 'invalid tester'
        }
        self.app.post_json('/accounts/', params=invalid_account2, headers=make_auth_header(), status=400)

        # Invalid Json format
        self.app.post_json('/accounts/', params=[], headers=make_auth_header(), status=400)

        # Trying to violate username and email uniqueness
        post_resp2 = self.app.post_json('/accounts/', params=valid_account, headers=make_auth_header()).json
        self.app.post_json('/accounts/', params=valid_account, headers=make_auth_header(), status=400)

        # Deleting twice
        self.app.delete('/accounts/%s' % post_resp2['id'], headers=make_auth_header())
        self.app.delete('/accounts/%s' % post_resp2['id'], headers=make_auth_header(), status=404)

        # Get with invalid account_id
        self.app.get('/accounts/%s' % 'invalid', headers=make_auth_header(), status=400)

        # Delete with invalid account_id
        self.app.delete('/accounts/%s' % 'invalid', headers=make_auth_header(), status=400)
