from django.contrib import admin
from api.models import (
    Exam,
    Question,
    Answer,
    UserQuestionResult,
    ResultSession
)

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(ResultSession)
admin.site.register(UserQuestionResult)
