from botorum.common import merge_dicts
from botorum.servicecatalog.models import BaseModel


class Product(BaseModel):

    _tag_options = []
    tags = {}

    @classmethod
    def list(cls, max_items=1000, page_size=20):
        paginator = cls.get_client().get_paginator('search_products_as_admin')
        response_iterator = paginator.paginate(
            SortBy='CreationDate',
            SortOrder='DESCENDING',
            ProductSource='ACCOUNT',
            PaginationConfig={'MaxItems': max_items, 'PageSize': page_size}
        )
        for response in response_iterator:
            for object_details in response.get('ProductViewDetails', []):
                flattened_details = cls._flatten_object_details(object_details)
                yield Product(**flattened_details)

    @classmethod
    def create(cls, **kwargs):
        """
        Create a new product and initial provisioning artifact (version).
        Arguments mirror the boto3 "create_product" API call, link below.
        Returns a Product object
        https://boto3.readthedocs.io/en/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.create_product
        """
        response = cls.get_client().create_product(**kwargs)
        object_details = cls._flatten_object_details(response)
        return cls(**object_details)

    @classmethod
    def get(cls, object_id):
        response = cls.get_client().describe_product_as_admin(Id=object_id)
        object_details = cls._flatten_object_details(response)
        return cls(**object_details)

    @staticmethod
    def _flatten_object_details(response):
        product_view_detail = response.get('ProductViewDetail', {})
        if 'ProductViewSummary' in product_view_detail:
            product_view_summary = product_view_detail.pop('ProductViewSummary', {})
        elif 'ProductViewSummary' in response:
            product_view_summary = response.get('ProductViewSummary', {})
        object_details = merge_dicts(product_view_detail, product_view_summary)
        if 'Tags' in response:
            object_details['tags'] = {x['Key']: x['Value'] for x in response.get('Tags', [])}
        return object_details

    def update(self, **kwargs):
        pass

    def delete(self):
        return self.client.delete_product(
            Id=self.product_id
        )

    class Meta(BaseModel.Meta):
        identity_attribute_name = 'product_id'
