#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `botorum.servicecatalog` package."""
import sys
import inspect
import pytest


from botorum.servicecatalog.portfolio import Portfolio


def test_classes_exist():
    assert inspect.isclass(Portfolio)


@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6")
def test_methods_exist():
    # TODO: Figure out why ismethod test fails
    assert inspect.isfunction(Portfolio.list)
    assert inspect.isfunction(Portfolio.create)
    assert inspect.isfunction(Portfolio.delete)
