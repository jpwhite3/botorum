from abc import ABC, abstractmethod
import boto3
from botorum.common import camel_to_snake


class BaseModel(ABC):

    session = boto3.Session()

    def __init__(self, **object_attrs):
        self._set_attrs(**object_attrs)

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

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self)

    def _set_attrs(self, **attrs):
        for attr, value in attrs.items():
            setattr(self, camel_to_snake(attr), value)

    @property
    def client(self):
        return self.session.client(self.Meta.boto3_client_name)

    @classmethod
    @abstractmethod
    def list(cls):
        pass

    @classmethod
    @abstractmethod
    def create(cls, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def get(cls, object_id):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    class Meta:
        boto3_client_name = 'servicecatalog'
        language = 'en'
