# -*- coding: utf-8 -*-
"""
Integration tests for the Account.

"""
from __future__ import unicode_literals

from nose.tools import eq_, ok_, assert_raises, assert_equal

from ave import model
from ave.model import DBSession
from ave.tests import TestController
from ave.tests.helpers import keep_keys


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
        post_resp = self.app.post('/accounts/', params=valid_account, status=200).json

        # Get the account just posted
        get_resp = self.app.get('/accounts/%s' % post_resp['id']).json
        eq_(
            keep_keys(['username', 'bio'], valid_account),
            keep_keys(['username', 'bio'], get_resp)
        )
        assert_equal(get_resp['reputation'], 0)
        assert_equal(get_resp['badges'], '')

        # Delete the account just got
        self.app.delete('/accounts/%s' % get_resp['id'])

        # Get the account just deleted
        self.app.get('/accounts/%s' % get_resp['id'], status=404)

        """BlackBox Testing"""

        # Typo in keys
        invalid_account = {
            'username': 'invalid',
            'passwosrd': 'invalid',
            'email_address': 'invalid@test.com',
            'bio': 'invalid tester'
        }
        self.app.post('/accounts/', params=invalid_account, status=400)

        # Dict lacking one pair
        invalid_account2 = {
            'username': 'invalid',
            'password': 'invalid',
            'bio': 'invalid tester'
        }
        self.app.post('/accounts/', params=invalid_account2, status=400)

        # Trying to violate username and email uniqueness
        post_resp2 = self.app.post('/accounts/', params=valid_account).json
        self.app.post('/accounts/', params=valid_account, status=400)

        # Deleting twice
        self.app.delete('/accounts/%s' % post_resp2['id'])
        self.app.delete('/accounts/%s' % post_resp2['id'], status=404)

        # Get with invalid account_id
        self.app.get('/accounts/%s' % 'invalid', status=400)

        # Delete with invalid account_id
        self.app.delete('/accounts/%s' % 'invalid', status=400)

