
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("info", views.info, name="info"),
    path("edit_info", views.edit_info, name="edit_info"),
    path("leave", views.leave, name="leave"),
]
