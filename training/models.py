from django.db import models
from django.contrib.auth.models import User

class Exum(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, default='')

class Question(models.Model):
    exum = models.ForeignKey(Exum, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)
    is_correct = models.BooleanField()

class UserQuestionResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exum = models.ForeignKey(Exum, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    answer_datetime = models.DateTimeField(auto_now_add=True)
