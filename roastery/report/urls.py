from django.urls import path

from . import views

app_name = "report"

urlpatterns = [
    path("bean-label/", view=views.generate_bean_label, name="bean-label"),
    path("roast-label/", view=views.generate_roast_label, name="roast-label"),
]
