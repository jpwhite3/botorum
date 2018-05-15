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


@pytest.fixture(scope="module")
def tag_options():
    return [
        {
            'Key': 'string',
            'Value': 'string',
            'Active': True | False,
            'Id': 'string'
        },
    ]


def test_classes_exist():
    assert inspect.isclass(Portfolio)


@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6")
def test_001_methods_exist():
    assert inspect.isfunction(Portfolio.__init__)
    assert inspect.isfunction(Portfolio.__getattr__)
    assert inspect.isfunction(Portfolio.__eq__)
    assert inspect.isfunction(Portfolio.__ne__)
    assert inspect.isfunction(Portfolio._Portfolio__set_attrs)
    assert inspect.isfunction(Portfolio._Portfolio__set_tags)
    assert inspect.isfunction(Portfolio._Portfolio__set_tag_options)
    assert inspect.isfunction(Portfolio._Portfolio__populate)
    assert inspect.isfunction(Portfolio._Portfolio__create)
    assert inspect.isfunction(Portfolio._Portfolio__load)
    assert inspect.isgeneratorfunction(Portfolio.list)
    assert inspect.isfunction(Portfolio.delete)
    assert isinstance(Portfolio.client, property)


def test_002_list_generator(portfolio_config):
    Portfolio(**portfolio_config)
    all_portfolios = [item for item in Portfolio.list()]
    assert len(all_portfolios) > 0
    assert isinstance(all_portfolios[0], Portfolio)


def test_003_instance_creation(portfolio_config):
    test_portfolio = Portfolio(**portfolio_config)
    assert test_portfolio.Id
    assert test_portfolio.ARN
    assert test_portfolio.CreatedTime
    assert test_portfolio.DisplayName == portfolio_config['DisplayName']
    assert test_portfolio.Description == portfolio_config['Description']
    assert test_portfolio.ProviderName == portfolio_config['ProviderName']

    tag_list = portfolio_config['Tags']
    assert test_portfolio.Tags == {x['Key']: x['Value'] for x in tag_list}


def test_004_instance_load(portfolio_config):
    test_portfolio = Portfolio(**portfolio_config)
    arbitrary_portfolio = Portfolio(portfolio_id=test_portfolio.Id)
    assert test_portfolio is not arbitrary_portfolio
    assert test_portfolio == arbitrary_portfolio
    assert not test_portfolio != arbitrary_portfolio

    assert arbitrary_portfolio.Id
    assert arbitrary_portfolio.ARN
    assert arbitrary_portfolio.CreatedTime
    assert arbitrary_portfolio.DisplayName == portfolio_config['DisplayName']
    assert arbitrary_portfolio.Description == portfolio_config['Description']
    assert arbitrary_portfolio.ProviderName == portfolio_config['ProviderName']

    tag_list = portfolio_config['Tags']
    assert arbitrary_portfolio.Tags == {x['Key']: x['Value'] for x in tag_list}


def test_005_tag_option_loading(portfolio_config, tag_options):
    test_portfolio = Portfolio(**portfolio_config)
    test_portfolio._Portfolio__set_tag_options(tag_options)
    assert len(test_portfolio.TagOptions) == 1

    actual_tag_options = test_portfolio.TagOptions[0]
    expected_tag_options = tag_options[0]
    assert actual_tag_options == expected_tag_options


def test_999_teardown():
    for p in Portfolio.list():
        portfolio = Portfolio(portfolio_id=p.Id)
        portfolio.delete()

    assert len([item for item in Portfolio.list()]) == 0
