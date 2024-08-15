from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("test_executive/", include("test_executive.urls")),
    path("admin/", admin.site.urls),
]
