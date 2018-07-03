import sys
import inspect
import pytest

from botorum.servicecatalog.models.portfolio import Portfolio
from botorum.servicecatalog.models.tagoption import TagOption


@pytest.fixture(scope="module")
def tagoption_config():
    return {
        'Key': 'test-portfolio-tagoption',
        'Value': 'arbitrary'
    }


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
    assert inspect.isfunction(Portfolio.__init__)
    assert inspect.isfunction(Portfolio.__getattr__)
    assert inspect.isfunction(Portfolio.__eq__)
    assert inspect.isfunction(Portfolio.__ne__)
    assert inspect.isfunction(Portfolio.__str__)
    assert inspect.isfunction(Portfolio.__unicode__)
    assert isinstance(Portfolio.client, property)
    assert inspect.isfunction(Portfolio._set_attrs)
    assert inspect.isfunction(Portfolio._flatten_object_details)
    assert inspect.isgeneratorfunction(Portfolio.list)
    assert inspect.ismethod(Portfolio.create)
    assert inspect.ismethod(Portfolio.get)
    assert inspect.ismethod(Portfolio.search)
    assert inspect.isfunction(Portfolio.update)
    assert inspect.isfunction(Portfolio.delete)
    assert inspect.isfunction(Portfolio.add_tag_option)
    assert inspect.isfunction(Portfolio.remove_tag_option)


def test_002_list_generator(portfolio_config):
    Portfolio.create(**portfolio_config)
    all_portfolios = [item for item in Portfolio.list()]
    assert len(all_portfolios) > 0
    assert isinstance(all_portfolios[0], Portfolio)


def test_002a_search(portfolio_config):
    search_term = portfolio_config['DisplayName']
    search_attr = 'DisplayName'
    results = Portfolio.search(search_attr, [search_term])
    assert len(results) == 1
    assert results[0].display_name == search_term


def test_003_instance_creation(portfolio_config):
    test_portfolio = Portfolio.create(**portfolio_config)
    assert str(test_portfolio) == str(test_portfolio.id)
    assert test_portfolio.__unicode__() == str(test_portfolio.id)


def test_004_instance_attributes(portfolio_config):
    test_portfolio = Portfolio.create(**portfolio_config)
    assert test_portfolio.Id == test_portfolio.id
    assert test_portfolio.ARN == test_portfolio.arn
    assert test_portfolio.CreatedTime == test_portfolio.created_time
    assert test_portfolio.DisplayName == test_portfolio.display_name
    assert test_portfolio.Description == test_portfolio.description
    assert test_portfolio.ProviderName == test_portfolio.provider_name
    assert test_portfolio.DisplayName == portfolio_config['DisplayName']
    assert test_portfolio.Description == portfolio_config['Description']
    assert test_portfolio.ProviderName == portfolio_config['ProviderName']

    with pytest.raises(AttributeError):
        assert test_portfolio.ArbitraryAttr

    tag_list = portfolio_config['Tags']
    assert test_portfolio.Tags == {x['Key']: x['Value'] for x in tag_list}


def test_005_instance_load(portfolio_config):
    test_portfolio = Portfolio.create(**portfolio_config)
    arbitrary_portfolio = Portfolio.get(test_portfolio.Id)
    assert test_portfolio is not arbitrary_portfolio
    assert test_portfolio == arbitrary_portfolio
    assert not test_portfolio != arbitrary_portfolio


def test_006_instance_update(portfolio_config):
    test_portfolio = Portfolio.create(**portfolio_config)
    assert test_portfolio.DisplayName == portfolio_config['DisplayName']
    assert test_portfolio.Description == portfolio_config['Description']
    assert test_portfolio.ProviderName == portfolio_config['ProviderName']
    assert test_portfolio.tags == {x['Key']: x['Value'] for x in portfolio_config['Tags']}

    update_params = {
        "DisplayName": "NewName",
        "Description": "NewDescription",
        "ProviderName": "NewProvider",
        "AddTags": [
            {
                'Key': 'example',
                'Value': 'example'
            },
        ],
        "RemoveTags": [
            "arbitrary"
        ]
    }
    test_portfolio.update(**update_params)
    assert test_portfolio.DisplayName == update_params["DisplayName"]
    assert test_portfolio.Description == update_params["Description"]
    assert test_portfolio.ProviderName == update_params["ProviderName"]
    assert test_portfolio.tags == {x['Key']: x['Value'] for x in update_params['AddTags']}


def test_007_add_tagoption(portfolio_config, tagoption_config):
    test_portfolio = Portfolio.create(**portfolio_config)
    test_tagoption = TagOption.get_or_create(**tagoption_config)

    test_portfolio.add_tag_option(test_tagoption)
    assert len(test_portfolio.tag_options) == 1
    assert test_portfolio.get_tag_option(test_tagoption.key)

    with pytest.raises(LookupError):
        assert test_portfolio.get_tag_option('NonExistantTagOptionKey')


def test_999_teardown():
    for p in Portfolio.list():
        portfolio = Portfolio(id=p.Id)
        portfolio.delete()
    assert len([item for item in Portfolio.list()]) == 0
