from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("members/", include("members.urls")),
    path("", views.main, name="main"),
    path("admin/", admin.site.urls),
]
