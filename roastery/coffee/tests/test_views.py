import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains

from ..views import BeanCreateView, BeanDetailView, BeanListView
from .factories import BeanFactory

pytestmark = pytest.mark.django_db


def test_good_bean_list_view_expanded(rf):
    request = rf.get(reverse("coffee:bean-list"))
    response = BeanListView.as_view()(request)
    assertContains(response, "Beans")


def test_good_bean_detail_view(rf):
    bean = BeanFactory()
    request = rf.get(reverse("coffee:bean-detail", kwargs={"slug": bean.slug}))
    response = BeanDetailView.as_view()(request, slug=bean.slug)
    assertContains(response, bean.name)


def test_good_bean_create_view(rf, admin_user):
    request = rf.get(reverse("coffee:bean-add"))
    request.user = admin_user
    response = BeanCreateView.as_view()(request)
    assert response.status_code == 200


def test_bean_list_contains_2_beans(rf):
    bean1 = BeanFactory()
    bean2 = BeanFactory()
    request = rf.get(reverse("coffee:bean-list"))
    response = BeanListView.as_view()(request)
    assertContains(response, bean1)
    assertContains(response, bean2)


def test_detail_contains_bean_data(rf):
    bean = BeanFactory()
    request = rf.get(reverse("coffee:bean-detail", kwargs={"slug": bean.slug}))
    response = BeanDetailView.as_view()(request, slug=bean.slug)
    assertContains(response, bean.name)
    assertContains(response, bean.country.flag)
