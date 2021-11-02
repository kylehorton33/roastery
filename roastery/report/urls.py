from django.urls import path

from . import views

app_name = "report"

urlpatterns = [
    path("hello/", view=views.some_view, name="hello"),
]
