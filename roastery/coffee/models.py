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
    green_weight = models.DecimalField(
        "Bean Mass (pre-roast) [g]", decimal_places=1, max_digits=5
    )
    roasted_weight = models.DecimalField(
        "Bean Mass (post-roast) [g]", decimal_places=1, max_digits=5
    )
    current_weight = models.DecimalField(
        "Current Mass [g]", decimal_places=1, max_digits=5
    )
    degree = models.CharField("Degree of Roast", max_length=20, choices=Degree.choices)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Created by User",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.green_bean.name} ({self.get_degree_display()} Roast)"

    def get_absolute_url(self):
        return reverse("coffee:roast-detail", kwargs={"slug": self.slug})

    def extractions(self):
        return Extraction.objects.filter(roasted_bean=self.id)

    def weight_loss(self):
        loss = (self.green_weight - self.roasted_weight) / self.green_weight
        return round(loss * 100, 1)

    def decrement(self, amount):
        if amount > self.current_weight:
            return self.current_weight
        else:
            self.current_weight -= amount
            self.save()
            return None

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
        FRENCH_PRESS = "french-press", "French Press"

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
    dose = models.DecimalField("Dose Weight [g]", decimal_places=1, max_digits=3)
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
    notes = models.TextField("Extra Notes", blank=True)

    def get_default_image(self, method):
        return {
            "espresso": {
                "uri": "/static/images/default/portafilter.png",
                "credit": '<p>Portafilter icon made by <a href="https://www.flaticon.com/authors/ultimatearm" \
                    title="ultimatearm">ultimatearm</a> from <a href="https://www.flaticon.com/" \
                    title="Flaticon">www.flaticon.com</a></p>',
            },
            "chemex": {
                "uri": "/static/images/default/chemex.png",
                "credit": '<p>Chemex icon made by <a href="https://www.flaticon.com/authors/pojok-d" \
                    title="pojok d">pojok d</a> from <a href="https://www.flaticon.com/" \
                    title="Flaticon">www.flaticon.com</a></p>',
            },
            "v60": {
                "uri": "/static/images/default/v60.png",
                "credit": '<p>V60 icon made by <a href="https://www.flaticon.com/authors/arana-stock" \
                    title="Arana_Stock">Arana_Stock</a> from <a href="https://www.flaticon.com/" \
                    title="Flaticon">www.flaticon.com</a></p>',
            },
            "french-press": {
                "uri": "/static/images/default/french-press.png",
                "credit": '<p>French Press icon made by <a href="https://www.flaticon.com/authors/xnimrodx" \
                    title="xnimrodx">xnimrodx</a> from <a href="https://www.flaticon.com/" \
                    title="Flaticon">www.flaticon.com</a></p>',
            },
        }[method]

    def __str__(self):
        return f"{self.get_method_display()}: {self.roasted_bean}"

    def get_absolute_url(self):
        return reverse("coffee:extraction-detail", kwargs={"slug": self.slug})

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return self.get_default_image(self.method)["uri"]

    def get_image_credit(self):
        if not self.image:
            return self.get_default_image(self.method)["credit"]
