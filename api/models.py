from django.db import models
from django.contrib.auth.models import User

class Exam(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, default='')
    pud_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.text

class ResultSession(models.Model):
    def __str__(self):
        return 'blank'

class UserQuestionResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    result_session = models.ForeignKey(ResultSession, on_delete=models.CASCADE)
    answer_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'blank'
