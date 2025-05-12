"""Views for accounts app"""


from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.template import loader
from django.views.generic.detail import Http404
from training.views import get_theme
from accounts.forms import ThemeForm
from api.models import UserPreference
from django.http import HttpResponse, HttpResponseRedirect


class SignUpView(CreateView):
    """Sign up view"""

    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class LogoutRedirectView(CreateView):
    """Logout redirect view"""

    def get(self, request):
        """Get method"""

        logout(request)
        return HttpResponseRedirect("/")


def preferences(request):
    """Preferences view"""

    if request.method == 'POST':
        form = ThemeForm(request.POST)
        if form.is_valid():
            theme_response = form.cleaned_data['theme']
            pref = UserPreference.objects.get(user=request.user)
            pref.theme = theme_response
            pref.save()
            return HttpResponseRedirect("/")
    else:
        template = loader.get_template("accounts/preferences.html")
        context = {
            'theme': get_theme(request),
            'form': ThemeForm(),
        }

        return HttpResponse(template.render(context, request))
