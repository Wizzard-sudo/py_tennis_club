from django.urls import path

from . import views

app_name = "members"
urlpatterns = [
    path("", views.MessageListView.as_view(), name="members"),
]
