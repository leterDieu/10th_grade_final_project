"""Views"""


from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from api.models import (
    Exam,
    Question,
    Answer,
    ResultSession,
    UserQuestionResult,
    UserPreference,
)
from api.serializers import (
    UserSerializer,
    ExamSerializer,
    QuestionSerializer,
    AnswerSerializer,
    ResultSessionSerializer,
    UserQuestionResultSerializer,
    UserPreferenceSerializer,
)
from utilities.exams import get_exam_stats


class UserViewSet(ModelViewSet):
    """User viewset"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserPreferenceViewSet(ModelViewSet):
    """User preference viewset"""

    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer


class ExamViewSet(ModelViewSet):
    """Exam viewset"""

    queryset = Exam.objects.all()
    serializer_class = ExamSerializer


class QuestionViewSet(ModelViewSet):
    """Question viewset"""

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(ModelViewSet):
    """Answer viewset"""

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class ResultSessionViewSet(ModelViewSet):
    """Result session viewset"""

    queryset = ResultSession.objects.all()
    serializer_class = ResultSessionSerializer


class UserQuestionResultViewSet(ModelViewSet):
    """User question result viewset"""

    queryset = UserQuestionResult.objects.all()
    serializer_class = UserQuestionResultSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]


class CreateUserView(CreateAPIView):
    """Create user view"""

    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


@permission_classes((permissions.AllowAny,))
class BlacklistRefreshView(APIView):
    """Blacklist refresh view"""

    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")


class HardestOverallExamView(View):
    """Hardest overall exam view"""

    def get(self, request):
        """Get method"""

        uqr = UserQuestionResult.objects.all().\
            select_related('answer').select_related('exam')
        uqr = uqr.annotate(is_correct_int=Cast('answer__is_correct',
                           IntegerField()))

        exam_stats_overall = get_exam_stats(uqr)

        return HttpResponse(exam_stats_overall['accuracy'][0]['id'])


class HardestUserExamView(View):
    """Hardest user exam view"""

    def get(self, request, user_id):
        """Get method"""

        uqr_users = UserQuestionResult.objects.filter(user=user_id).\
            select_related('answer').select_related('exam')
        uqr_users = uqr_users.annotate(is_correct_int=Cast(
                                       'answer__is_correct',
                                       IntegerField()))

        exam_stats_users = get_exam_stats(uqr_users)

        if len(exam_stats_users['accuracy']):
            return HttpResponse(exam_stats_users['accuracy'][0]['id'])
        return HttpResponseBadRequest('No user found')
