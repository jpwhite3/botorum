import sys
import inspect
import pytest

from botorum.servicecatalog.models.tagoption import TagOption


@pytest.fixture(scope="module")
def tagoption_config():
    return {
        'Key': 'arbitrary',
        'Value': 'arbitrary'
    }


def test_classes_exist():
    assert inspect.isclass(TagOption)


@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6")
def test_001_methods_exist():
    assert inspect.isfunction(TagOption.__init__)
    assert inspect.isfunction(TagOption.__getattr__)
    assert inspect.isfunction(TagOption.__eq__)
    assert inspect.isfunction(TagOption.__ne__)
    assert inspect.isfunction(TagOption.__str__)
    assert inspect.isfunction(TagOption.__unicode__)
    assert inspect.isgeneratorfunction(TagOption.list)
    assert inspect.ismethod(TagOption.create)
    assert inspect.ismethod(TagOption.get)
    assert inspect.ismethod(TagOption.get_or_create)
    assert inspect.isfunction(TagOption.update)
    assert inspect.isfunction(TagOption.delete)
    assert isinstance(TagOption.client, property)


def test_002_list_generator(tagoption_config):
    test_tagoption = TagOption.create(**tagoption_config)
    all_tagoptions = [item for item in TagOption.list()]
    assert len(all_tagoptions) == 1
    assert isinstance(all_tagoptions[0], TagOption)
    assert test_tagoption == all_tagoptions[0]


def test_003_instance_creation(tagoption_config):
    test_tagoption = TagOption.get_or_create(**tagoption_config)
    assert str(test_tagoption) == str(test_tagoption.id)
    assert test_tagoption.__unicode__() == str(test_tagoption.id)


def test_004_instance_attributes(tagoption_config):
    test_tagoption = TagOption.get_or_create(**tagoption_config)
    assert test_tagoption.Id == test_tagoption.id
    assert test_tagoption.Key == test_tagoption.key
    assert test_tagoption.Value == test_tagoption.value
    assert test_tagoption.Active == test_tagoption.active

    with pytest.raises(AttributeError):
        assert test_tagoption.ArbitraryAttr


def test_005_instance_load(tagoption_config):
    test_tagoption = TagOption.get_or_create(**tagoption_config)
    arbitrary_tagoption = TagOption.get(test_tagoption.Id)
    assert test_tagoption is not arbitrary_tagoption
    assert test_tagoption == arbitrary_tagoption
    assert not test_tagoption != arbitrary_tagoption


def test_999_teardown():
    for p in TagOption.list():
        tagoption = TagOption(id=p.Id)
        tagoption.delete()

    assert len([item for item in TagOption.list()]) == 0
