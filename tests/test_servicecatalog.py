#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `botorum.servicecatalog` package."""
import inspect
# import pytest


from botorum.servicecatalog.portfolio import Portfolio


def test_classes_exist():
    assert inspect.isclass(Portfolio)


def test_properties_exist():
    assert inspect.isfunction(Portfolio.create)


def test_methods_exist():
    # TODO: Figure out why ismethod test fails
    assert inspect.isfunction(Portfolio.list)
    assert inspect.isfunction(Portfolio.create)
    assert inspect.isfunction(Portfolio.delete)
