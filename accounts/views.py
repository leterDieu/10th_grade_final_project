from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.template import loader
from django.views.generic.detail import Http404
from training.views import theme_is_light
from accounts.forms import ThemeForm
from api.models import UserPreference
from django.http import HttpResponse, HttpResponseRedirect


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
def preferences(request):
    if request.method == 'POST':
        form = ThemeForm(request.POST)
        if form.is_valid():
            theme_is_light_response = form.cleaned_data['theme_is_light']
            pref = UserPreference.objects.get(user=request.user)
            pref.theme_is_light = theme_is_light_response
            pref.save()
            return HttpResponseRedirect("/")
    else:
        template = loader.get_template("accounts/preferences.html")
        context = {
            'theme_is_light': theme_is_light(request),
            'form': ThemeForm(),
        }

        return HttpResponse(template.render(context, request))
