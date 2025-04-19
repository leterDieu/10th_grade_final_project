"""Urls for training app"""


from django.urls import path
from training.views import (
    index,
    exams_page,
    exam,
    exam_content,
    exam_result
)

urlpatterns = [
    path('', index, name='index'),
    path('exam/', exams_page, name='exams_page'),
    path('exam/<int:exam_id>/', exam, name='exam'),
    path('exam/<int:exam_id>/content/', exam_content, name='exam_content'),
    path('exam/<int:result_session_id>/result/',
         exam_result, name='exam_result'),
]
