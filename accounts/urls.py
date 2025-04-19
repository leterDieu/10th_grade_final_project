"""Urls for accounts app"""


from django.urls import path
from accounts.views import SignUpView, preferences


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("preferences/", preferences, name="preferences"),
]
