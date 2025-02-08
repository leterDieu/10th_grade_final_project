from django.urls import path, include
from api.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('exam', ExamViewSet, basename='exam')
router.register('question', QuestionViewSet, basename='question')
router.register('answer', AnswerViewSet, basename='answer')
router.register('user_question_result', UserQuestionResultViewSet, basename='user_question_result')

urlpatterns = [
    path('', include(router.urls)),
]
