"""All the models used in the project"""


from django.db import models
from django.contrib.auth.models import User


class Exam(models.Model):
    """Exam (test) model"""

    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, default='')
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.name)


class Question(models.Model):
    """Question model, pointing to the exam it belongs to"""

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)

    def __str__(self) -> str:
        return str(self.text)


class Answer(models.Model):
    """Answer model, pointing to the question it belongs to"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)
    is_correct = models.BooleanField()

    def __str__(self) -> str:
        return str(self.text)


class ResultSession(models.Model):
    """Empty model to store sessions"""
    def __str__(self) -> str:
        return 'blank'


class UserQuestionResult(models.Model):
    """Model that contains all the recordings of users' answers"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    result_session = models.ForeignKey(ResultSession, on_delete=models.CASCADE)
    answer_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return 'blank'


class UserPreference(models.Model):
    """User's preferences such as theme model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=16)

    def __str__(self) -> str:
        return str(self.theme)
