from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import (
    Exam,
    Question,
    Answer,
    ResultSession,
    UserQuestionResult
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        # 'first_name', 'last_name', 'email', 'date_joined'

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'name', 'description']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'exam', 'text']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'text', 'is_correct']

class ResultSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultSession
        fields = ['id']

class UserQuestionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestionResult
        fields = ['id', 'user', 'exam', 'question', 'answer', 'answer_datetime']
