from autoslug import AutoSlugField
from django.conf import settings
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from model_utils.models import TimeStampedModel


class Bean(TimeStampedModel):
    name = models.CharField("Name of Bean", max_length=255)
    slug = AutoSlugField(
        "Bean URL slug", unique=True, always_update=False, populate_from="name"
    )
    country = CountryField("Country of Origin")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Created by User",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Return absolute URL to the Cheese Detail page."""
        return reverse("coffee:bean-detail", kwargs={"slug": self.slug})
