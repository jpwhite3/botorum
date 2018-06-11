from botorum.servicecatalog.models import BaseModel


class Portfolio(BaseModel):

    @classmethod
    def list(cls, max_items=1000, page_size=20):
        """
        Generator function that iterates over all portfolios in the account. Paginates 20 items per API call by default, the max as of this writing.
        Returns Portfolio object.
        https://boto3.readthedocs.io/en/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListPortfolios
        """

        paginator = cls.get_client().get_paginator('list_portfolios')
        response_iterator = paginator.paginate(
            AcceptLanguage=cls.Meta.language,
            PaginationConfig={'MaxItems': max_items, 'PageSize': page_size}
        )
        for response in response_iterator:
            for object_detail in response.get('PortfolioDetails'):
                yield cls(**object_detail)

    @classmethod
    def create(cls, **kwargs):
        """
        Create a new portfolio.
        Arguments mirror the boto3 "create_portfolio" API call, link below.
        Returns a Portfolio object.
        https://boto3.readthedocs.io/en/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.create_portfolio
        """

        response = cls.get_client().create_portfolio(**kwargs)
        object_details = response.get('PortfolioDetail', {})
        object_details['tags'] = {x['Key']: x['Value'] for x in response.get('Tags', [])}
        return cls(**object_details)

    @classmethod
    def get(cls, object_id):
        """
        Get a portfolio by Id.
        Returns a Portfolio object.
        """

        client = cls.session.client(cls.Meta.boto3_client_name)
        response = client.describe_portfolio(AcceptLanguage=cls.Meta.language, Id=object_id)
        object_details = cls._flatten(response)
        object_details['tag_options'] = response.get('TagOptions', [])
        return cls(**object_details)

    @staticmethod
    def _flatten(response):
        object_details = response.get('PortfolioDetail', {})
        object_details['tags'] = {x['Key']: x['Value'] for x in response.get('Tags', [])}
        return object_details

    def update(self, **kwargs):
        """
        Updates the following attributes of the Portfolio object: DisplayName, Description, ProviderName, Tags
        Returns the Portfolio object.
        Argument(s) mirror the boto3 "update_portfolio" API call, link below.
        https://boto3.readthedocs.io/en/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.update_portfolio
        """
        response = self.client.update_portfolio(
            AcceptLanguage=self.Meta.language,
            Id=self.id,
            DisplayName=kwargs.get('DisplayName', self.display_name),
            Description=kwargs.get('Description', self.description),
            ProviderName=kwargs.get('ProviderName', self.provider_name),
            AddTags=kwargs.get('AddTags', []),
            RemoveTags=kwargs.get('RemoveTags', [])
        )
        object_details = self._flatten(response)
        self._set_attrs(**object_details)

    def delete(self):
        """
        Delete this portfolio object by calling boto3 delete_potfolio.
        https://boto3.readthedocs.io/en/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.delete_portfolio
        """
        return self.client.delete_portfolio(
            AcceptLanguage=self.Meta.language,
            Id=self.id
        )
