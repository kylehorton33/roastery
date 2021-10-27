import pytest

from .factories import BeanFactory, ExtractionFactory, RoastFactory

pytestmark = pytest.mark.django_db


def test_bean__str__():
    bean = BeanFactory()
    assert bean.__str__() == bean.name
    assert str(bean) == bean.name


def test_bean_get_absolute_url():
    bean = BeanFactory()
    url = bean.get_absolute_url()
    assert url == f"/coffee/beans/{bean.slug}/"


def test_roast__str__():
    roast = RoastFactory()
    assert roast.__str__() == f"{roast.get_degree_display()} - {roast.green_bean.name}"
    assert str(roast) == f"{roast.get_degree_display()} - {roast.green_bean.name}"


def test_extraction__str__():
    extraction = ExtractionFactory()
    assert (
        extraction.__str__()
        == f"{extraction.get_method_display()}: {extraction.roasted_bean}"
    )
    assert (
        str(extraction)
        == f"{extraction.get_method_display()}: {extraction.roasted_bean}"
    )
