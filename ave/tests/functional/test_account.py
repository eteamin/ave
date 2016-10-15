# -*- coding: utf-8 -*-
"""
Integration tests for the Account.

"""
from __future__ import unicode_literals

from nose.tools import eq_, ok_

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
        assert get_resp['reputation'] == 0
        assert get_resp['badges'] == ''

        # Delete the account just got
        self.app.delete('/accounts/%s' % get_resp['id'])

        # Get the account just deleted
        self.app.get('/accounts/%s' % get_resp['id'], status=404)
