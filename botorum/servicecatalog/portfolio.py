import boto3


class Portfolio(object):

    client = boto3.client('servicecatalog')
    language = 'en'

    @classmethod
    def list(cls, MaxItems=1000, PageSize=20):
        """
        Generator function that lists all portfolios in the account.
        Paginates 20 items per page by default, the max as of this writing.

        Keyword Arguments:
            MaxItems {int} -- The total # of items to return (default: {1000})
            PageSize {int} -- The size of each page (default: {20})
        """

        paginator = cls.client.get_paginator('list_portfolios')
        response_iterator = paginator.paginate(
            AcceptLanguage=cls.language,
            PaginationConfig={'MaxItems': MaxItems, 'PageSize': PageSize}
        )
        for response in response_iterator:
            for portfolio_detail in response.get('PortfolioDetails'):
                yield portfolio_detail

    def __init__(self, **kwargs):
        portfolio_id = kwargs.pop('portfolio_id', None)
        if portfolio_id:
            self.__load(portfolio_id)
        else:
            self.__create(**kwargs)

    def __set_attrs(self, **attrs):
        for attr, value in attrs.items():
            setattr(self, attr, value)

    def __set_tags(self, tag_list):
        if tag_list:
            tag_dict = {x['Key']: x['Value'] for x in tag_list}
            setattr(self, 'Tags', tag_dict)

    def __set_tag_options(self, tag_option_list):
        if tag_option_list:
            setattr(self, 'TagOptions', tag_option_list)

    def __populate(self, response):
        attrs = response.get('PortfolioDetail', {})
        tags = response.get('Tags', [])
        tag_options = response.get('TagOptions', [])
        self.__set_attrs(**attrs)
        self.__set_tags(tags)
        self.__set_tag_options(tag_options)

    def __create(self, **kwargs):
        response = self.client.create_portfolio(**kwargs)
        self.__populate(response)

    def __load(self, portfolio_id):
        response = self.client.describe_portfolio(
            AcceptLanguage=self.language,
            Id=portfolio_id
        )
        self.__populate(response)

    def delete(self):
        return self.client.delete_portfolio(
            AcceptLanguage=self.language,
            Id=self.Id
        )
