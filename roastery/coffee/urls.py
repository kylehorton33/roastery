from django.urls import path

from . import views

app_name = "coffee"
urlpatterns = [
    path(route="beans/", view=views.BeanListView.as_view(), name="bean-list"),
    path(route="beans/add/", view=views.BeanCreateView.as_view(), name="bean-add"),
    path(
        route="beans/<slug:slug>/",
        view=views.BeanDetailView.as_view(),
        name="bean-detail",
    ),
    path(
        route="beans/<slug:slug>/update/",
        view=views.BeanUpdateView.as_view(),
        name="bean-update",
    ),
    path(
        route="beans/<slug:slug>/delete/",
        view=views.BeanDeleteView.as_view(),
        name="bean-delete",
    ),
]
