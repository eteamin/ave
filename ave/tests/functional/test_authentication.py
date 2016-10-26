# -*- coding: utf-8 -*-
"""
Integration tests for the :mod:`repoze.who`-powered authentication sub-system.

As ave grows and the authentication method changes, only these tests
should be updated.

"""

from nose.tools import eq_, ok_

from ave.tests import TestController


class TestAuthentication(TestController):
    """
    Tests for the default authentication setup.

    If your application changes how the authentication layer is configured
    those tests should be updated accordingly
    """

    application_under_test = 'main'
