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

    def test_post_account(self):
        """Account Posting Test"""

        # Posting a valid account
        valid_account = {
            'username': 'test',
            'password': 'test',
            'email_address': 'test@test.com',
            'bio': 'tester'
        }
        self.app.post('/account/new', params=valid_account, status=200)
        # Get the account just posted
        get_resp = self.app.get('/account/1')
        eq_(
            keep_keys(['username', 'bio'], valid_account),
            keep_keys(['username', 'bio'], get_resp)
        )
        assert get_resp['reputation'] == 0
        assert get_resp['badges'] == ''

