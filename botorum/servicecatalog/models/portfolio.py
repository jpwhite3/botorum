from botorum.servicecatalog.models import BaseModel


class Portfolio(BaseModel):

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

        client = cls.session.client(cls.Meta.boto3_client_name)
        paginator = client.get_paginator('list_portfolios')
        response_iterator = paginator.paginate(
            AcceptLanguage=cls.Meta.language,
            PaginationConfig={'MaxItems': max_items, 'PageSize': page_size}
        )
        for response in response_iterator:
            for object_detail in response.get('PortfolioDetails'):
                yield cls(**object_detail)

    @classmethod
    def create(cls, **kwargs):
        client = cls.session.client(cls.Meta.boto3_client_name)
        response = client.create_portfolio(**kwargs)
        object_details = response.get('PortfolioDetail', {})
        object_details['tags'] = {x['Key']: x['Value'] for x in response.get('Tags', [])}
        return cls(**object_details)

    @classmethod
    def get(cls, portfolio_id):
        client = cls.session.client(cls.Meta.boto3_client_name)
        response = client.describe_portfolio(AcceptLanguage=cls.Meta.language, Id=portfolio_id)
        object_details = response.get('PortfolioDetail', {})
        object_details['tags'] = {x['Key']: x['Value'] for x in response.get('Tags', [])}
        object_details['tag_options'] = response.get('TagOptions', [])
        return cls(**object_details)

    def update(self):
        pass

    def delete(self):
        """
        Delete this portfolio object by calling boto3 delete_potfolio.
        https://boto3.readthedocs.io/en/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.delete_portfolio

        Returns:
            Dict -- Empty dict from boto3 response
        """
        return self.client.delete_portfolio(
            AcceptLanguage=self.Meta.language,
            Id=self.id
        )
