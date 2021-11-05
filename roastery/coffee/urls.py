from django.urls import include, path

from . import views

app_name = "coffee"

bean_urlpatterns = [
    path(route="", view=views.BeanListView.as_view(), name="bean-list"),
    path(route="add/", view=views.BeanCreateView.as_view(), name="bean-add"),
    path(
        route="<slug:slug>/",
        view=views.BeanDetailView.as_view(),
        name="bean-detail",
    ),
    path(
        route="<slug:slug>/update/",
        view=views.BeanUpdateView.as_view(),
        name="bean-update",
    ),
    path(
        route="<slug:slug>/delete/",
        view=views.BeanDeleteView.as_view(),
        name="bean-delete",
    ),
]

roast_urlpatterns = [
    path(route="", view=views.RoastListView.as_view(), name="roast-list"),
    path(route="add/", view=views.RoastCreateView.as_view(), name="roast-add"),
    path(
        route="<slug:slug>/",
        view=views.RoastDetailView.as_view(),
        name="roast-detail",
    ),
    path(
        route="<slug:slug>/update/",
        view=views.RoastUpdateView.as_view(),
        name="roast-update",
    ),
    path(
        route="<slug:slug>/delete/",
        view=views.RoastDeleteView.as_view(),
        name="roast-delete",
    ),
]

extraction_urlpatterns = [
    path(route="", view=views.ExtractionListView.as_view(), name="extraction-list"),
    path(
        route="add/", view=views.ExtractionCreateView.as_view(), name="extraction-add"
    ),
    path(
        route="<slug:slug>/",
        view=views.ExtractionDetailView.as_view(),
        name="extraction-detail",
    ),
    path(
        route="<slug:slug>/update/",
        view=views.ExtractionUpdateView.as_view(),
        name="extraction-update",
    ),
    path(
        route="<slug:slug>/delete/",
        view=views.ExtractionDeleteView.as_view(),
        name="extraction-delete",
    ),
]

urlpatterns = [
    path("beans/", include(bean_urlpatterns)),
    path("roasts/", include(roast_urlpatterns)),
    path("extractions/", include(extraction_urlpatterns)),
]
