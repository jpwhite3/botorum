#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `botorum` package."""

import pytest


from botorum import botorum
from botorum import cloudformation


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

def test_hello():
    assert botorum.hello('world') == "Hello world"
