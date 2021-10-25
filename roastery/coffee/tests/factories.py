import factory
import factory.fuzzy
from django.template.defaultfilters import slugify

from ..models import Bean


class BeanFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))

    class Meta:
        model = Bean
