import abc
import six
import boto3
from botorum.common import camel_to_snake


@six.add_metaclass(abc.ABCMeta)
class BaseModel():

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
        return self.__str__()

    def _set_attrs(self, **attrs):
        for attr, value in attrs.items():
            setattr(self, camel_to_snake(attr), value)

    @property
    def client(self):
        return self.__class__.get_client()

    @classmethod
    def get_client(cls):
        return cls.session.client(cls.Meta.boto3_client_name)

    @classmethod
    @abc.abstractmethod
    def list(cls, max_items=1000, page_size=20):
        pass

    @classmethod
    @abc.abstractmethod
    def create(cls, **kwargs):
        pass

    @classmethod
    @abc.abstractmethod
    def get(cls, object_id):
        pass

    @classmethod
    def search(cls, attribute, search_terms):
        assert search_terms, "At least one search term must exist"
        search_results = []
        for obj in cls.list():
            attr_value = getattr(obj, attribute, "")
            for search_term in search_terms:
                if attr_value and search_term.lower() in attr_value.lower():
                    search_results.append(obj)
        return search_results

    @abc.abstractmethod
    def update(self, **kwargs):
        pass

    @abc.abstractmethod
    def delete(self):
        pass

    class Meta:
        boto3_client_name = 'servicecatalog'
        language = 'en'
