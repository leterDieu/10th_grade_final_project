import requests
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Avg
from django.views import View
from django.http import HttpResponse
from api.models import (
    Exam,
    Question,
    Answer,
    UserQuestionResult
)
from api.serializers import (
    UserSerializer,
    ExamSerializer,
    QuestionSerializer,
    AnswerSerializer,
    UserQuestionResultSerializer
)


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

class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

@permission_classes((permissions.AllowAny,))
class BlacklistRefreshView(APIView):
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")

class GetHardestUserExam(View):
    def get(self, request, user_id):
        cursor = connection.cursor()
        cursor.execute(
            f'''SELECT uqr.exam_id
            FROM api_userquestionresult AS uqr
            JOIN api_answer AS a
            ON uqr.answer_id = a.id
            GROUP BY uqr.exam_id
            HAVING uqr.user_id = {user_id}
            ORDER BY AVG(CAST(a.is_correct AS INTEGER))
            LIMIT 1;''')

        res = cursor.fetchone()
        return HttpResponse(res)
