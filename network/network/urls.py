
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("all_posts", views.all_posts, name="all_posts"),
    path("following_posts", views.following_posts, name="following_posts"),
    path("edit/<str:user>/<int:post_id>", views.edit_post, name="edit"),
    path("profile/<str:user>", views.profile, name="profile"),

    # API Route
    path("users/<str:user>", views.users, name="users"),
    path("like/<str:user>", views.like, name="like"),
]
