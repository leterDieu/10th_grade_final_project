from django.contrib import admin

from .models import Exam, Question, Answer, UserQuestionResult

admin.site.register([Exam, Question, Answer, UserQuestionResult])
