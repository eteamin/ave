# -*- coding: utf-8 -*-
"""
Integration tests for decorators.

"""
from tg import config
from nose.tools import eq_, assert_equal
from pyDes import triple_des, des

from ave.tests import TestController
from ave.tests.helpers import keep_keys


class TestDecorators(TestController):
    """
    Tests for the decorators.

    """
    application_under_test = 'main'

    def test_is_authorized(self):
        """is_authorized test"""
        secret_key = config.get('auth_secret_key')
        auth_message = config.get('auth_message')
        cipher_text = triple_des(secret_key).encrypt(auth_message, padmode=2)
        invalid_cipher_text = triple_des(secret_key).encrypt("I am not a kivy user", padmode=2)

        # Get with authentication
        self.app.get('/users/require_authentication', params={}, headers={'token': cipher_text})

        # Get with invalid authentication
        self.app.get('/users/require_authentication', status=401)
        self.app.get('/users/require_authentication', headers={'toke': cipher_text}, status=401)
        self.app.get('/users/require_authentication', headers={'token': invalid_cipher_text}, status=401)
