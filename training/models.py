from django.db import models
from django.contrib.auth.models import User

class Test(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, default='')

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)
    is_correct = models.BooleanField()

class UserResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # test_id

class UserQuestionResult(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user_result = models.ForeignKey(UserResult, on_delete=models.CASCADE)
