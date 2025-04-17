from django import forms
from django.contrib.auth.models import User
from api.models import UserPreference


class ThemeForm(forms.Form):
    theme_is_light = forms.ChoiceField(choices=[(True, 'Light'), (False, 'Dark')])
