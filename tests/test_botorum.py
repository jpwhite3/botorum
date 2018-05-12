#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `botorum` package."""
import inspect


from botorum import servicecatalog
from botorum.servicecatalog import portfolio, product


def test_servicecatalog_package_exists():
    assert inspect.ismodule(servicecatalog)


def test_servicecatalog_modules_exists():
    assert inspect.ismodule(portfolio)
    assert inspect.ismodule(product)
