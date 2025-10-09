"""URL patterns for plans app."""
from django.urls import path

from . import views

app_name = "plans"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="project-list"),
    path("projects/<int:pk>/", views.ProjectDetailView.as_view(), name="project-detail"),
    path("projects/<int:pk>/sections/<str:table_key>/", views.SectionDataView.as_view(), name="section-data"),
    path(
        "projects/<int:pk>/sections/<str:table_key>/rows/",
        views.SectionRowView.as_view(),
        name="section-rows",
    ),
    path(
        "projects/<int:pk>/sections/<str:table_key>/rows/<int:row_id>/",
        views.SectionRowView.as_view(),
        name="section-row-detail",
    ),
]
