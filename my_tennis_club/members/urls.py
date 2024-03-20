from django.urls import path

from . import views

app_name = "members"
urlpatterns = [
    path("", views.MemberListView.as_view(), name="members-list"),
    path("get/<pk>/", views.MemberRetrieveAPIView.as_view(), name="member-get"),
    path("create/", views.MemberCreateView.as_view(), name="members-save"),
    path("update/<pk>", views.MemberUpdateView.as_view(), name="members-update"),
]
