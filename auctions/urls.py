from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("listings/", views.listings, name="listings"),
    path("listings/<int:listing_id>", views.listing_detail, name="listing_detail"),
    path("listings/<int:listing_id>/add_comment", views.add_comment, name="add_comment"),
    path("listings/<int:listing_id>/place_bid", views.place_bid, name="place_bid"),
    path("listings/<int:listing_id>/add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("listings/<str:category>", views.listings, name="filtered_listings"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/delete/<int:listing_id>", views.delete_from_watchlist, name="delete_from_watchlist"),
    path("listings/<int:listing_id>/delete", views.delete_listing, name="delete_listing"),
    path("listings/<int:listing_id>/close", views.close_auction, name="close_auction")
]

