from django import template
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from rest_framework.request import HttpRequest
from api.models import (
    Exam,
    Question,
    Answer,
    ResultSession,
    UserQuestionResult
)
from django.db.models.functions import Cast
from django.db.models import IntegerField
import random
from training.forms import QuestionForm, BaseQuestionFormSet
from django.forms import formset_factory


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
    }

    return HttpResponse(template.render(context, request))


def exam_content(request, exam_id):
    question_objects = Question.objects.filter(exam_id=exam_id)

    question_id_list = [question.id for question in question_objects]

    QuestionFormSet = formset_factory(form=QuestionForm,
        formset=BaseQuestionFormSet,
        extra=len(question_id_list))

    if request.method == 'POST':
        formset = QuestionFormSet(request.POST, form_kwargs={
            'question_id_list': question_id_list
        })
        if formset.is_valid():
            result_session_object = ResultSession.objects.create()
            result_session_id = result_session_object.id
            for i, form in enumerate(formset):
                cd = form.cleaned_data
                answer_id_local = cd.get('answer')
                if answer_id_local is None:
                    continue

                question_id = question_id_list[i]
                question_object = Question.objects.get(id=question_id)

                answer_correct = Answer.objects.get(question=question_id, is_correct=True)
                answer_objects = Answer.objects.all()\
                .filter(question_id=question_id)
                answer_choices = [answer.id for answer in answer_objects]
                answer_id = answer_choices[int(answer_id_local)]
                answer_object = Answer.objects.get(id=answer_id)

                exam_object = Exam.objects.get(question=question_id)

                user_object = request.user

                uqr = UserQuestionResult.objects.create(
                    user=user_object,
                    question=question_object,
                    answer=answer_object,
                    exam=exam_object,
                    result_session=result_session_object,
                )
                uqr.save()

            return redirect(f'/exam/{result_session_id}/result/', request)

    else:
        formset = QuestionFormSet(form_kwargs={
            'question_id_list': question_id_list
        })

        template = loader.get_template("training/exam_content.html")
        context = {
            'formset': formset,
        }

        return HttpResponse(template.render(context, request))

def exam_result(request, result_session_id):
    if request.method == 'POST':
        pass
    else:
        uqr_objects = UserQuestionResult.objects.filter(result_session=result_session_id)
        answers_info = []
        for uqr in uqr_objects:
            right_answer_text = Answer.objects.get(question=uqr.question.id, is_correct=True).text
            answers_info.append(
                f'''
                question: {uqr.question.text},
                user answer: {uqr.answer.text},
                right answer: {right_answer_text},
                is correct: {uqr.answer.is_correct}
                '''
            )
        return HttpResponse(answers_info)
