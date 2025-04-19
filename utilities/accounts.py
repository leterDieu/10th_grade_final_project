"""Utilities for accounts"""


from api.models import UserPreference


def theme_is_light(request):
    """Check user's theme"""
    try:
        return UserPreference.objects.get(user=request.user).theme_is_light
    except Exception as e:
        return True
