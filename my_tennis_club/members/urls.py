from django.urls import path

from . import views

app_name = "members"
urlpatterns = [
    path("", views.MemberListView.as_view(), name="members-list"),
    path("create/", views.MemberCreateView.as_view(), name="members-save"),
]
