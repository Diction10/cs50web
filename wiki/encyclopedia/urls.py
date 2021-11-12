from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_page", views.new_page, name="new_page"),
    path("search", views.search, name="search"),
    path("random_page", views.random_page, name="random_page"),
    path("edit_page/<str:title>", views.edit_page, name="edit_page"),
    path("<str:title>", views.title_page, name="title_page"),
    
]
