from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/watch", views.watcher, name="watcher"),
    path("listing/<int:listing_id>/bid", views.bid, name="bid"),
    path("listing/<int:listing_id>/close", views.is_active, name="is_active"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:name>", views.category, name="category"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment")
]
