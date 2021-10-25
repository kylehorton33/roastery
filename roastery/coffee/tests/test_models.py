import pytest

from .factories import BeanFactory

pytestmark = pytest.mark.django_db


def test_bean__str__():
    bean = BeanFactory()
    assert bean.__str__() == bean.name
    assert str(bean) == bean.name


def test_bean_get_absolute_url():
    bean = BeanFactory()
    url = bean.get_absolute_url()
    assert url == f"/coffee/beans/{bean.slug}"
