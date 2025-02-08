from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from api.models import *
from api.serializers import *


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExamViewSet(ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class UserQuestionResultViewSet(ModelViewSet):
    queryset = UserQuestionResult.objects.all()
    serializer_class = UserQuestionResultSerializer
