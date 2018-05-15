import boto3
from ..common import camel_to_snake


class Portfolio(object):

    session = boto3.Session()
    language = 'en'

    @property
    def client(self):
        return self.session.client('servicecatalog')

    @classmethod
    def list(cls, max_items=1000, page_size=20):
        """
        Generator function that lists all portfolios in the account.
        Paginates 20 items per page by default, the max as of this writing.
        https://boto3.readthedocs.io/en/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListPortfolios

        Keyword Arguments:
            MaxItems {int} -- The total # of items to return (default: {1000})
            PageSize {int} -- The size of each page (default: {20})

        Returns:
            Dict -- Portfolio details from boto3 response
        """

        client = cls.session.client('servicecatalog')
        paginator = client.get_paginator('list_portfolios')
        response_iterator = paginator.paginate(
            AcceptLanguage=cls.language,
            PaginationConfig={'MaxItems': max_items, 'PageSize': page_size}
        )
        for response in response_iterator:
            for portfolio_detail in response.get('PortfolioDetails'):
                portfolio_id = portfolio_detail['Id']
                yield Portfolio(portfolio_id=portfolio_id)

    def __init__(self, **kwargs):
        portfolio_id = kwargs.pop('portfolio_id', None)
        if portfolio_id:
            self.__load(portfolio_id)
        else:
            self.__create(**kwargs)

    def __getattr__(self, name):
        attr_name = camel_to_snake(name)
        try:
            return self.__dict__[attr_name]
        except KeyError:
            raise AttributeError("Attribute not found")

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __set_attrs(self, **attrs):
        for attr, value in attrs.items():
            setattr(self, camel_to_snake(attr), value)

    def __set_tags(self, tag_list):
        if tag_list:
            tag_dict = {x['Key']: x['Value'] for x in tag_list}
            setattr(self, 'tags', tag_dict)

    def __set_tag_options(self, tag_option_list):
        if tag_option_list:
            setattr(self, 'tag_options', tag_option_list)

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
        """
        Delete this portfolio object by calling boto3 delete_potfolio.
        https://boto3.readthedocs.io/en/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.delete_portfolio

        Returns:
            Dict -- Empty dict from boto3 response
        """
        return self.client.delete_portfolio(
            AcceptLanguage=self.language,
            Id=self.id
        )
