from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist_page", views.watchlist_page, name="watchlist_page"),
    path("category", views.category, name="category"),
    path("category_list/<str:name>", views.category_list, name="category_list"),
    path("watchlist/<str:name>", views.watchlist, name="watchlist"),
    path("remove_watchlist/<str:name>", views.remove_watchlist, name="remove_watchlist"),
    path("listing_page/<str:name>", views.listing_page, name="listing_page"),
    path("bid/<str:name>", views.bid, name="bid"),
    path("close_auction/<str:name>", views.close_auction, name="close_auction"),
    
    
]
