"""Urls' config for api, e.g. /api/"""


from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from api.views import (
    ResultSessionViewSet,
    UserViewSet,
    ExamViewSet,
    QuestionViewSet,
    AnswerViewSet,
    UserQuestionResultViewSet,
    CreateUserView,
    BlacklistRefreshView,
    HardestUserExamView,
    HardestOverallExamView,
    UserPreferenceViewSet,
)


APP_NAME = 'api'

router = routers.DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('exam', ExamViewSet, basename='exam')
router.register('question', QuestionViewSet, basename='question')
router.register('answer', AnswerViewSet, basename='answer')
router.register('resultsession',
                ResultSessionViewSet,
                basename='resultsession')
router.register('userquestionresult',
                UserQuestionResultViewSet,
                basename='userquestionresult')
router.register('userpreference',
                UserPreferenceViewSet,
                basename='userpreference')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', CreateUserView.as_view(), name='create_user'),
    path('logout/', BlacklistRefreshView.as_view(), name='token_blacklist'),
    path('hardest_user_exam/<int:user_id>/', HardestUserExamView.as_view(),
         name='hardest_user_exam'),
    path('hardest_overall_exam/', HardestOverallExamView.as_view(),
         name='hardest_overall_exam'),
]
