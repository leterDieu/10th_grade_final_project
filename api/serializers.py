"""Serializers"""


import dataclasses
from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import (
    Exam,
    Question,
    Answer,
    ResultSession,
    UserQuestionResult,
    UserPreference,
)


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        """Custom create method"""

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    @dataclasses.dataclass
    class Meta:
        """Meta"""

        model = User
        fields = ['id', 'username', 'password']


class ExamSerializer(serializers.ModelSerializer):
    """Exam seializer"""

    @dataclasses.dataclass
    class Meta:
        """Meta"""

        model = Exam
        fields = ['id', 'name', 'description']


class QuestionSerializer(serializers.ModelSerializer):
    """Question serializer"""

    @dataclasses.dataclass
    class Meta:
        """Meta"""

        model = Question
        fields = ['id', 'exam', 'text']


class AnswerSerializer(serializers.ModelSerializer):
    """Answer serializer"""

    @dataclasses.dataclass
    class Meta:
        """Meta"""

        model = Answer
        fields = ['id', 'question', 'text', 'is_correct']


class ResultSessionSerializer(serializers.ModelSerializer):
    """Result session serializer"""

    @dataclasses.dataclass
    class Meta:
        """Meta"""

        model = ResultSession
        fields = ['id']


class UserQuestionResultSerializer(serializers.ModelSerializer):
    """Recording's of user's answers serializer"""

    @dataclasses.dataclass
    class Meta:
        """Meta"""

        model = UserQuestionResult
        fields = [
            'id', 'user', 'exam',
            'question', 'answer', 'answer_datetime'
        ]


class UserPreferenceSerializer(serializers.ModelSerializer):
    """User preference serializer"""

    @dataclasses.dataclass
    class Meta:
        """Meta"""

        model = UserPreference
        fields = ['id', 'user', 'theme']
