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
from django.db.models import Avg, IntegerField
from django.db.models.functions import Cast
from django.views import View
from django.http import HttpResponse
from api.models import (
    Exam,
    Question,
    Answer,
    ResultSession,
    UserQuestionResult
)
from api.serializers import (
    UserSerializer,
    ExamSerializer,
    QuestionSerializer,
    AnswerSerializer,
    ResultSessionSerializer,
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

class ResultSessionViewSet(ModelViewSet):
    queryset = ResultSession.objects.all()
    serializer_class = ResultSessionSerializer

class UserQuestionResultViewSet(ModelViewSet):
    queryset = UserQuestionResult.objects.all()
    serializer_class = UserQuestionResultSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

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

class HardestUserExamView(View):
    def get(self, request, user_id):
        uqr = UserQuestionResult.objects.filter(user_id=user_id).\
        select_related('answer')
        as_int = uqr.annotate(is_correct_int = Cast('answer__is_correct', IntegerField()))
        accs_lists = {}
        for acc in as_int:
            if acc.exam_id not in accs_lists:
                accs_lists[acc.exam_id] = []
            accs_lists[acc.exam_id].append(acc.is_correct_int)

        accs = {}
        for acc_exam_id, acc_accs in accs_lists.items():
            accs[acc_exam_id] = sum(acc_accs) / len(acc_accs)

        accs_sorted = sorted(accs.items(), key=lambda item: item[1])

        return HttpResponse(accs_sorted[0][0])

class HardestOverallExamView(View):
    def get(self, request):
        uqr = UserQuestionResult.objects.all().\
        select_related('answer')
        as_int = uqr.annotate(is_correct_int = Cast('answer__is_correct', IntegerField()))
        accs_lists = {}
        for acc in as_int:
            if acc.exam_id not in accs_lists:
                accs_lists[acc.exam_id] = []
            accs_lists[acc.exam_id].append(acc.is_correct_int)

        accs = {}
        for acc_exam_id, acc_accs in accs_lists.items():
            accs[acc_exam_id] = sum(acc_accs) / len(acc_accs)

        accs_sorted = sorted(accs.items(), key=lambda item: item[1])

        return HttpResponse(accs_sorted[0][0])
