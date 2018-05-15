# -*- coding: utf-8 -*-

"""Tests for `botorum.common` package."""
from botorum.common import camel_to_snake


def test_camel_to_snake():
    assert camel_to_snake('CamelCase') == 'camel_case'
    assert camel_to_snake('CamelCamelCase') == 'camel_camel_case'
    assert camel_to_snake('Camel2Camel2Case') == 'camel2_camel2_case'
    assert camel_to_snake('getHTTPResponseCode') == 'get_http_response_code'
    assert camel_to_snake('get2HTTPResponseCode') == 'get2_http_response_code'
    assert camel_to_snake('HTTPResponseCode') == 'http_response_code'
    assert camel_to_snake('HTTPResponseCodeXYZ') == 'http_response_code_xyz'
