from django.urls import path

from . import views

app_name = "coffee"
urlpatterns = [
    path(route="beans/", view=views.BeanListView.as_view(), name="bean-list"),
    path(route="beans/add/", view=views.BeanCreateView.as_view(), name="bean-add"),
    path(
        route="beans/<slug:slug>",
        view=views.BeanDetailView.as_view(),
        name="bean-detail",
    ),
]
