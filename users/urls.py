from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register_user/", views.registration, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.settings, name="profile"),
]
