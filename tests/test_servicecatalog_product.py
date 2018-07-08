import sys
import inspect
import time
import pytest

from botorum.servicecatalog.models.product import Product


@pytest.fixture(scope="module")
def tagoption_config():
    return {
        'Key': 'test-product-tagoption',
        'Value': 'arbitrary'
    }


@pytest.fixture(scope="module")
def product_config():
    return {
        'Name': 'arbitrary',
        'Owner': 'arbitrary',
        'Description': 'arbitrary',
        'Distributor': 'arbitrary',
        'SupportDescription': 'arbitrary',
        'SupportEmail': 'dummy@example.com',
        'SupportUrl': 'http://www.example.com',
        'ProductType': 'CLOUD_FORMATION_TEMPLATE',
        'Tags': [
            {
                'Key': 'arbitrary',
                'Value': 'arbitrary'
            },
        ],
        'ProvisioningArtifactParameters': {
            'Name': 'arbitrary',
            'Description': 'arbitrary',
            'Info': {
                'LoadTemplateFromURL': 'https://s3.amazonaws.com/jpw3-public/test_stack.cfn.json'
            },
            'Type': 'CLOUD_FORMATION_TEMPLATE'
        }
    }


def test_classes_exist():
    assert inspect.isclass(Product)


@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6")
def test_001_methods_exist():
    assert inspect.isfunction(Product.__init__)
    assert inspect.isfunction(Product.__getattr__)
    assert inspect.isfunction(Product.__eq__)
    assert inspect.isfunction(Product.__ne__)
    assert inspect.isfunction(Product.__str__)
    assert inspect.isfunction(Product.__unicode__)
    assert isinstance(Product.client, property)
    assert inspect.isfunction(Product._set_attrs)
    assert inspect.isfunction(Product._flatten_object_details)
    assert inspect.isgeneratorfunction(Product.list)
    assert inspect.ismethod(Product.create)
    assert inspect.ismethod(Product.get)
    assert inspect.ismethod(Product.search)
    assert inspect.isfunction(Product.update)
    assert inspect.isfunction(Product.delete)
    # assert isinstance(Product.tag_options, property)
    # assert inspect.isfunction(Product.add_tag_option)
    # assert inspect.isfunction(Product.remove_tag_option)


def test_002_list_generator(product_config):
    Product.create(**product_config)
    time.sleep(5)
    all_products = [item for item in Product.list()]
    assert len(all_products) == 1
    assert isinstance(all_products[0], Product)


def test_003_instance_creation(product_config):
    test_product = Product.create(**product_config)
    assert str(test_product) == str(test_product.product_id)
    assert test_product.__unicode__() == str(test_product.product_id)


def test_004_instance_attributes(product_config):
    test_product = Product.create(**product_config)
    assert test_product.Id == test_product.id
    assert test_product.ProductId == test_product.product_id
    assert test_product.Name == test_product.name
    assert test_product.Owner == test_product.owner
    assert test_product.ShortDescription == test_product.short_description
    assert test_product.Type == test_product.type
    assert test_product.Distributor == test_product.distributor
    assert test_product.HasDefaultPath == test_product.has_default_path
    assert test_product.SupportEmail == test_product.support_email
    assert test_product.SupportDescription == test_product.support_description
    assert test_product.SupportUrl == test_product.support_url
    assert test_product.Status == test_product.status
    assert test_product.ProductARN == test_product.product_arn
    assert test_product.CreatedTime == test_product.created_time

    with pytest.raises(AttributeError):
        assert test_product.ArbitraryAttr

    tag_list = product_config['Tags']
    assert test_product.Tags == {x['Key']: x['Value'] for x in tag_list}


def test_005_instance_load(product_config):
    test_product = Product.create(**product_config)
    arbitrary_product = Product.get(test_product.product_id)
    assert test_product is not arbitrary_product
    assert test_product == arbitrary_product
    assert not test_product != arbitrary_product


@pytest.mark.teardown
def test_999_teardown():
    time.sleep(10)
    for product in Product.list():
        product.delete()
    time.sleep(10)
    assert len([item for item in Product.list()]) == 0
