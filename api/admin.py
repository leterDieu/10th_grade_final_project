from django.contrib import admin
from api.models import (
    Exam,
    Question,
    Answer,
    UserQuestionResult
)

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserQuestionResult)
