from botorum.servicecatalog.models import BaseModel


class TagOption(BaseModel):

    @classmethod
    def list(cls, max_items=1000, page_size=20):
        paginator = cls.get_client().get_paginator('list_tag_options')
        response_iterator = paginator.paginate(
            PaginationConfig={'MaxItems': max_items, 'PageSize': page_size}
        )
        for response in response_iterator:
            for object_details in response.get('TagOptionDetails', []):
                yield TagOption(**object_details)

    @classmethod
    def create(cls, **kwargs):
        response = cls.get_client().create_tag_option(**kwargs)
        object_details = response.get('TagOptionDetail', {})
        return cls(**object_details)

    @classmethod
    def get(cls, object_id):
        response = cls.get_client().describe_tag_option(Id=object_id)
        object_details = response.get('TagOptionDetail', {})
        return cls(**object_details)

    @classmethod
    def get_or_create(cls, **kwargs):
        response = cls.get_client().list_tag_options(Filters=kwargs)
        tagoption_details = response.get('TagOptionDetails', [])
        if tagoption_details:
            return cls(**tagoption_details[0])
        return cls.create(**kwargs)

    def update(self, **kwargs):
        response = self.client.update_tag_option(
            Id=self.id,
            Value=kwargs.get('Value', self.value),
            Active=kwargs.get('Active', self.active),
        )
        object_details = response.get('TagOptionDetail', {})
        self._set_attrs(**object_details)

    def delete(self):
        return self.client.delete_tag_option(
            Id=self.id
        )
