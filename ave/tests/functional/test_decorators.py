# -*- coding: utf-8 -*-
"""
Integration tests for decorators.

"""
from tg import config
from pyDes import triple_des
from nose.tools import assert_equal

from ave.tests import TestController
from ave.tests.helpers import make_auth_header


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
        get_resp = self.app.get('/users/require_authentication', headers=make_auth_header()).json
        assert_equal(get_resp['OK'], True)

        # Get with invalid authentication
        self.app.get('/users/require_authentication', status=401)
        self.app.get('/users/require_authentication', headers={'toke': cipher_text}, status=401)
        self.app.get('/users/require_authentication', headers={'token': invalid_cipher_text}, status=401)
