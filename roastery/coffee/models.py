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
        """Return absolute URL to the Bean Detail page."""
        return reverse("coffee:bean-detail", kwargs={"slug": self.slug})


class Roast(TimeStampedModel):
    class Degree(models.TextChoices):
        CINNAMON = "cinnamon", "Cinnamon"
        CITY = "city", "City"
        CITY_PLUS = "city-plus", "City Plus"
        FULL_CITY = "full-city", "Full City"
        VIENNA = "vienna", "Vienna"
        ESPRESSO = "espresso", "Espresso"
        ITALIAN = "italian", "Italian"

    green_bean = models.ForeignKey(Bean, verbose_name="Bean", on_delete=models.CASCADE)
    slug = AutoSlugField(
        "Roast URL slug", unique=True, always_update=False, populate_from="__str__"
    )
    degree = models.CharField("Degree of Roast", max_length=20, choices=Degree.choices)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Created by User",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.get_degree_display()} - {self.green_bean.name}"


class Extraction(TimeStampedModel):
    class Method(models.TextChoices):
        ESPRESSO = "espresso", "Espresso"
        V60 = "v60", "V60"
        CHEMEX = "chemex", "Chemex"

    class Grinder(models.TextChoices):
        NICHE_ZERO = "niche-zero", "Niche Zero"
        BARATZA_ENCORE = "baratza_encore", "Baratza Encore"
        HARIO_MINI_MILL = "hario-mini-mill", "Hario Mini Mill"

    roasted_bean = models.ForeignKey(
        Roast, verbose_name="Roasted Bean", on_delete=models.CASCADE
    )
    method = models.CharField(
        "Method of Extraction",
        max_length=20,
        choices=Method.choices,
        default=Method.ESPRESSO,
    )
    grinder = models.CharField(
        "Grinder", max_length=20, choices=Grinder.choices, default=Grinder.NICHE_ZERO
    )
    grind_setting = models.DecimalField(
        "Grinder Coarseness Setting", decimal_places=1, max_digits=3
    )
    temperature = models.DecimalField(
        "Temperature of Extraction [°C]", decimal_places=1, max_digits=3
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Created by User",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.get_method_display()}: {self.roasted_bean}"
