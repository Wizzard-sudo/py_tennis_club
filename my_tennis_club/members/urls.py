from django.urls import path

from . import views

app_name = "members"
urlpatterns = [
    path("", views.MemberListView.as_view(), name="members-list"),
    path("<int:id>/", views.get_member_by_id, name="member-get"),
    path("create/", views.MemberCreateView.as_view(), name="members-save"),
]
