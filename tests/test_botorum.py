import inspect
from botorum import servicecatalog
from botorum.servicecatalog.models import portfolio, product, tagoption


def test_servicecatalog_package_exists():
    assert inspect.ismodule(servicecatalog)


def test_servicecatalog_modules_exists():
    assert inspect.ismodule(portfolio)
    assert inspect.ismodule(product)
    assert inspect.ismodule(tagoption)
