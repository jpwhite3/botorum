from botorum.servicecatalog.models import BaseModel
from botorum.servicecatalog.models.tagoption import TagOption
from botorum.common import lazy_property


class Portfolio(BaseModel):

    _tag_options = []
    tags = {}

    @classmethod
    def list(cls, max_items=1000, page_size=20):
        """
        Generator function that iterates over all portfolios in the account.
        Returns Portfolio object.
        https://boto3.readthedocs.io/en/latest/reference/services/servicecatalog.html#ServiceCatalog.Paginator.ListPortfolios
        """

        paginator = cls.get_client().get_paginator('list_portfolios')
        response_iterator = paginator.paginate(
            AcceptLanguage=cls.Meta.language,
            PaginationConfig={'MaxItems': max_items, 'PageSize': page_size}
        )
        for response in response_iterator:
            for object_detail in response.get('PortfolioDetails', []):
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
        object_details = cls._flatten_object_details(response)
        return cls(**object_details)

    @classmethod
    def get(cls, object_id):
        """
        Get a portfolio by Id.
        Returns a Portfolio object.
        """

        response = cls.get_client().describe_portfolio(AcceptLanguage=cls.Meta.language, Id=object_id)
        object_details = cls._flatten_object_details(response)
        return cls(**object_details)

    @staticmethod
    def _flatten_object_details(response):
        object_details = response.get('PortfolioDetail', {})
        if 'Tags' in response:
            object_details['tags'] = {x['Key']: x['Value'] for x in response.get('Tags', [])}
        return object_details

    @lazy_property
    def tag_options(self):
        response = self.client.describe_portfolio(AcceptLanguage=self.Meta.language, Id=self.id)
        self._tag_options = [TagOption(**x) for x in response.get('TagOptions', [])]
        return self._tag_options

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
        object_details = self._flatten_object_details(response)
        self._set_attrs(**object_details)

    def delete(self):
        """
        Delete this portfolio object by calling boto3 delete_potfolio.
        https://boto3.readthedocs.io/en/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.delete_portfolio
        """
        # Remove all tag_options
        for tag_option in self.tag_options:
            self.remove_tag_option(tag_option)

        return self.client.delete_portfolio(
            AcceptLanguage=self.Meta.language,
            Id=self.id
        )

    def get_tag_option(self, key):
        for tag_option in self._tag_options:
            if tag_option.key == key:
                return tag_option
        raise LookupError('TagOption with key [%s] not associated to this portfolio' % key)

    def add_tag_option(self, tagoption):
        try:
            self.client.associate_tag_option_with_resource(
                ResourceId=self.id,
                TagOptionId=tagoption.id
            )
            self._tag_options.append(tagoption)
        except self.client.exceptions.DuplicateResourceException:
            pass
        return {}

    def remove_tag_option(self, tagoption):
        try:
            self.client.disassociate_tag_option_from_resource(
                ResourceId=self.id,
                TagOptionId=tagoption.id
            )
            self._tag_options.remove(tagoption)
        except self.client.exceptions.ResourceNotFoundException:
            pass
        return {}
