#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `botorum` package."""
import inspect
import pytest


from botorum import servicecatalog
from botorum.servicecatalog import portfolio, product


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


def test_servicecatalog_package_exists():
    assert inspect.ismodule(servicecatalog)


def test_servicecatalog_modules_exists():
    assert inspect.ismodule(portfolio)
    assert inspect.ismodule(product)
