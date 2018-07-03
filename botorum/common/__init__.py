import re


def camel_to_snake(camel_string):
    """[summary]

    Arguments:
        camel_string {string} -- String in CamelCase

    Returns:
        string -- snake_cased version of CamelCase string
    """

    sub1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', sub1).lower()


def lazy_property(func):
    '''Decorator that makes a property lazy-evaluated.'''
    attr_name = '_lazy_' + func.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    return _lazy_property
