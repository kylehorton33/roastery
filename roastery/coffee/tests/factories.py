import factory
import factory.fuzzy
from django.template.defaultfilters import slugify

from roastery.users.tests.factories import UserFactory

from ..models import Bean


class BeanFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    country = factory.Faker("country_code")
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Bean
