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
