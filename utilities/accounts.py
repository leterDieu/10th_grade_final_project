"""Utilities for accounts"""


from api.models import UserPreference


def get_theme(request):
    """Gets user's theme"""

    try:
        return UserPreference.objects.get(user=request.user).theme
    except Exception as e:
        return 'latte'
