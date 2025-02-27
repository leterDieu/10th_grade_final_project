from django.urls import path, include
from rest_framework import routers
from api.views import (
    UserViewSet,
    ExamViewSet,
    QuestionViewSet,
    AnswerViewSet,
    UserQuestionResultViewSet,
    CreateUserView,
    BlacklistRefreshView,
    GetHardestUserExam
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = routers.DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('exam', ExamViewSet, basename='exam')
router.register('question', QuestionViewSet, basename='question')
router.register('answer', AnswerViewSet, basename='answer')
router.register('userquestionresult', UserQuestionResultViewSet, basename='userquestionresult')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', CreateUserView.as_view(), name='create_user'),
    path('logout/', BlacklistRefreshView.as_view(), name='token_blacklist'),
    path('hardest_exam/<int:user_id>', GetHardestUserExam.as_view(), name='hardest_exam')
]
