import factory
import factory.fuzzy
from django.template.defaultfilters import slugify

from roastery.users.tests.factories import UserFactory

from ..models import Bean, Extraction, Roast


class BeanFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    country = factory.Faker("country_code")
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Bean


ROAST_DEGREE_CHOICES = [x[0] for x in Roast.Degree]


class RoastFactory(factory.django.DjangoModelFactory):
    green_bean = factory.SubFactory(BeanFactory)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.__str__))
    degree = factory.fuzzy.FuzzyChoice(ROAST_DEGREE_CHOICES)
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Roast


EXTRACTION_METHOD_CHOICES = [x[0] for x in Extraction.Method]
EXTRACTION_GRINDER_CHOICES = [x[0] for x in Extraction.Grinder]


class ExtractionFactory(factory.django.DjangoModelFactory):
    roasted_bean = factory.SubFactory(RoastFactory)
    method = factory.fuzzy.FuzzyChoice(EXTRACTION_METHOD_CHOICES)
    grinder = factory.fuzzy.FuzzyChoice(EXTRACTION_GRINDER_CHOICES)
    grind_setting = factory.Faker("pydecimal", left_digits=2, right_digits=1)
    temperature = factory.Faker("pydecimal", left_digits=2, right_digits=1)
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Extraction
