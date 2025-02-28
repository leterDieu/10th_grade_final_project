from django.urls import path

from training.views import (
    index,
    exam,
    exam_content
)

urlpatterns = [
    path('', index, name='index'),
    path('exam/<int:exam_id>/', exam, name='exam'),
    path('exam/<int:exam_id>/content/', exam_content, name='exam_content'),
]
