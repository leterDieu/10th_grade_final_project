from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Exam

def index(request):
    exams = Exam.objects.all()[:5]

    template = loader.get_template("training/index.html")
    context = {
        "exams": exams,
    }
    return HttpResponse(template.render(context, request))
