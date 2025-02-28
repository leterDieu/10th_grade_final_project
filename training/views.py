from django import template
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from api.models import (
    Exam,
    Question,
    Answer,
    UserQuestionResult
)
from django.db.models.functions import Cast
from django.db.models import IntegerField
import random


def index(request, top_n: int = 5):
    uqr = UserQuestionResult.objects.all().\
    select_related('answer').select_related('exam')
    uqr = uqr.annotate(is_correct_int = Cast('answer__is_correct', IntegerField()))

    exam_stats = {}
    for el in uqr:
        if el.exam_id not in exam_stats:
            exam_stats[el.exam_id] = {'name': el.exam.name,
                'answers': 0,
                'correct_answers': 0}
        exam_stats[el.exam_id]['answers'] += 1
        exam_stats[el.exam_id]['correct_answers'] += el.is_correct_int

    exam_stats_by_accuracy = dict(sorted(
        exam_stats.items(),
        key=lambda item:
            item[1]['correct_answers'] / item[1]['answers']))

    exam_stats_by_popularity = dict(sorted(
        exam_stats.items(),
        key=lambda item:
            item[1]['answers'],
        reverse=True))

    exam_stats_by_accuracy_readable = [
        {'number': i + 1,
            'id': id,
            'name': el['name'],
            'accuracy': round(el['correct_answers'] / el['answers'], 3) * 100}
        for i, (id, el) in enumerate(exam_stats_by_accuracy.items())]

    exam_stats_by_popularity_readable = [
        {'number': i + 1,
            'id': id,
            'name': el['name'],
            'answers': el['answers']}
        for i, (id, el) in enumerate(exam_stats_by_popularity.items())]

    template = loader.get_template("training/index.html")
    context = {
        'exam_stats_by_accuracy_readable': exam_stats_by_accuracy_readable[:top_n],
        'exam_stats_by_popularity_readable': exam_stats_by_popularity_readable[:top_n],
        'top_n': top_n,
    }

    return HttpResponse(template.render(context, request))

def exam(request, exam_id):
    exam_object = Exam.objects.get(id=exam_id)

    template = loader.get_template("training/exam.html")
    context = {
        'name': exam_object.name,
        'description': exam_object.description,
        'exam_id': exam_id,
    }

    return HttpResponse(template.render(context, request))

def exam_content(request, exam_id):
    question_objects = Question.objects.all()\
    .select_related('exam').filter(exam_id=exam_id)

    question_object = random.choice(question_objects)

    # add dependency from UserQuestionResult
    # add form-like display for Answers

    template = loader.get_template("training/exam_content.html")
    context = {
        'text': question_object.text,
    }

    return HttpResponse(template.render(context, request))
