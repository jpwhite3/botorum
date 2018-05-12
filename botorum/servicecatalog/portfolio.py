import boto3


class Portfolio(object):

    client = boto3.client('servicecatalog')
    config = dict()

    @classmethod
    def list(cls, AcceptLanguage='en', MaxItems=1000, PageSize=20):
        paginator = cls.client.get_paginator('list_portfolios')
        response_iterator = paginator.paginate(
            AcceptLanguage=AcceptLanguage,
            PaginationConfig={'MaxItems': MaxItems, 'PageSize': PageSize}
        )
        for response in response_iterator:
            for portfolio_detail in response.get('PortfolioDetails'):
                yield portfolio_detail

    def __init__(self, **kwargs):
        portfolio_id = kwargs.pop('portfolio_id', None)
        self.config['default_language'] = kwargs.get('AcceptLanguage', 'en')
        if portfolio_id:
            self.__load(portfolio_id)
        else:
            self.__create(**kwargs)

    def __setattrs__(self, **attrs):
        for attr, value in attrs.items():
            setattr(self, attr, value)

    def __create(self, **kwargs):
        response = self.client.create_portfolio(**kwargs)
        portfolio_attrs = response.get('PortfolioDetail', {})
        self.__setattrs__(**portfolio_attrs)

    def __load(self, portfolio_id):
        response = self.client.describe_portfolio(
            AcceptLanguage=self.config['default_language'],
            Id=portfolio_id
        )
        portfolio_attrs = response.get('PortfolioDetail', {})
        self.__setattrs__(**portfolio_attrs)

    def delete(self):
        return self.client.delete_portfolio(
            AcceptLanguage=self.config['default_language'],
            Id=self.Id
        )
