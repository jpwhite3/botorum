#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `botorum.servicecatalog` package."""
import sys
import inspect
import pytest

from botorum.servicecatalog.portfolio import Portfolio


@pytest.fixture(scope="module")
def portfolio_config():
    return {
        'DisplayName': 'arbitrary',
        'Description': 'arbitrary',
        'ProviderName': 'arbitrary',
        'Tags': [
            {
                'Key': 'arbitrary',
                'Value': 'arbitrary'
            },
        ]
    }


def test_classes_exist():
    assert inspect.isclass(Portfolio)


@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6")
def test_001_methods_exist():
    # TODO: Figure out why ismethod test fails
    assert inspect.isfunction(Portfolio.__init__)
    assert inspect.isfunction(Portfolio.__setattrs__)
    assert inspect.isfunction(Portfolio._Portfolio__create)
    assert inspect.isfunction(Portfolio._Portfolio__load)
    assert inspect.isgeneratorfunction(Portfolio.list)
    assert inspect.isfunction(Portfolio.delete)


def test_002_list_generator():
    all_portfolios = [item for item in Portfolio.list()]
    assert len(all_portfolios) == 0


def test_003_instance_creation_and_deletion(portfolio_config):
    test_portfolio = Portfolio(**portfolio_config)
    assert len([item for item in Portfolio.list()]) == 1

    assert test_portfolio.Id
    assert test_portfolio.ARN
    assert test_portfolio.CreatedTime
    assert test_portfolio.DisplayName == portfolio_config['DisplayName']
    assert test_portfolio.Description == portfolio_config['Description']
    assert test_portfolio.ProviderName == portfolio_config['ProviderName']

    assert test_portfolio.delete()
    assert len([item for item in Portfolio.list()]) == 0


def test_004_instance_load(portfolio_config):
    assert len([item for item in Portfolio.list()]) == 0

    test_portfolio = Portfolio(**portfolio_config)
    arbitrary_portfolio = Portfolio(portfolio_id=test_portfolio.Id)
    assert len([item for item in Portfolio.list()]) == 1

    assert test_portfolio is not arbitrary_portfolio
    assert test_portfolio.Id == arbitrary_portfolio.Id
    assert test_portfolio.Id
    assert test_portfolio.ARN
    assert test_portfolio.CreatedTime
    assert test_portfolio.DisplayName == portfolio_config['DisplayName']
    assert test_portfolio.Description == portfolio_config['Description']
    assert test_portfolio.ProviderName == portfolio_config['ProviderName']

    test_portfolio.delete()
    assert len([item for item in Portfolio.list()]) == 0
