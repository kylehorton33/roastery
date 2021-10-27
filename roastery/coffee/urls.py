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
    path(route="roasts/", view=views.RoastListView.as_view(), name="roast-list"),
    path(route="roasts/add/", view=views.RoastCreateView.as_view(), name="roast-add"),
    path(
        route="roasts/<slug:slug>/",
        view=views.RoastDetailView.as_view(),
        name="roast-detail",
    ),
    path(
        route="roasts/<slug:slug>/update/",
        view=views.RoastUpdateView.as_view(),
        name="roast-update",
    ),
    path(
        route="roasts/<slug:slug>/delete/",
        view=views.RoastDeleteView.as_view(),
        name="roast-delete",
    ),
]
