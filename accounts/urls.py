"""Urls for accounts app"""


from django.urls import path
from accounts.views import (
    SignUpView,
    preferences,
    LogoutRedirectView,
)


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("preferences/", preferences, name="preferences"),
    path('logout_redirect/', LogoutRedirectView.as_view(),
         name='logout_redirect')
]
