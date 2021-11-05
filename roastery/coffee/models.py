from autoslug import AutoSlugField
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_countries.fields import CountryField
from model_utils.models import TimeStampedModel


class Bean(TimeStampedModel):
    name = models.CharField("Name of Bean", max_length=255)
    slug = AutoSlugField(
        "Bean URL slug", unique=True, always_update=False, populate_from="name"
    )
    country = CountryField("Country of Origin")
    description = models.TextField("Description of Bean", blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Created by User",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    def roasts(self):
        return Roast.objects.filter(green_bean=self.id)

    def get_absolute_url(self):
        return reverse("coffee:bean-detail", kwargs={"slug": self.slug})

    def get_label_data(self):
        host = f"https://{settings.ALLOWED_HOSTS[0]}"  # this works in production if host is the only/first ALLOWED_HOST
        if settings.DEBUG:
            host = f"http://{settings.ALLOWED_HOSTS[-1]}:8000"  # if running locally, host is development machine
        full_url = f"{host}{self.get_absolute_url()}"
        data = {"name": self.name, "origin": self.country.name, "url": full_url}
        return data


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
    roast_date = models.DateField(default=timezone.now)
    degree = models.CharField("Degree of Roast", max_length=20, choices=Degree.choices)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Created by User",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.get_degree_display()} - {self.green_bean.name}"

    def get_absolute_url(self):
        return reverse("coffee:roast-detail", kwargs={"slug": self.slug})

    def extractions(self):
        return Extraction.objects.filter(roasted_bean=self.id)

    def get_label_data(self):
        host = f"https://{settings.ALLOWED_HOSTS[0]}"  # this works in production if host is the only/first ALLOWED_HOST
        if settings.DEBUG:
            host = f"http://{settings.ALLOWED_HOSTS[-1]}:8000"  # if running locally, host is development machine
        full_url = f"{host}{self.get_absolute_url()}"
        data = {
            "name": self.green_bean,
            "roast": self.get_degree_display(),
            "origin": self.green_bean.country.name,
            "roast_date": self.roast_date,
            "url": full_url,
        }
        return data


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
    slug = AutoSlugField(
        "Extraction URL slug", unique=True, always_update=False, populate_from="__str__"
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
    image = models.ImageField(upload_to="extraction/", null=True)

    def get_default_image(self, method):
        return {
            "espresso": "/static/images/default/portafilter.png",
            "v60": "/static/images/default/v60.png",
            "chemex": "/static/images/default/chemex.png",
        }[method]

    def __str__(self):
        return f"{self.get_method_display()}: {self.roasted_bean}"

    def get_absolute_url(self):
        return reverse("coffee:extraction-detail", kwargs={"slug": self.slug})

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return self.get_default_image(self.method)
