"""Views for training app"""


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
    UserQuestionResult,
    UserPreference,
)
from django.db.models.functions import Cast
from django.db.models import IntegerField
import random
from training.forms import QuestionForm, BaseQuestionFormSet
from django.forms import formset_factory
import pandas as pd
from typing import Any
from utilities.exams import get_exam_stats
from utilities.accounts import get_theme


def index(request):
    """Index view"""

    template = loader.get_template("training/index.html")
    context = {
        'theme': get_theme(request)
    }

    return HttpResponse(template.render(context, request))


def exams_page(request, top_n: int = 5, latest_n: int = 10):
    """Exams page view"""

    uqr = UserQuestionResult.objects.all().\
        select_related('answer').select_related('exam')
    uqr = uqr.annotate(is_correct_int=Cast('answer__is_correct',
                                           IntegerField()))

    uqr_users = UserQuestionResult.objects.filter(user=request.user.id).\
        select_related('answer').select_related('exam')
    uqr_users = uqr_users.annotate(is_correct_int=Cast('answer__is_correct',
                                                       IntegerField()))

    exam_stats_overall = get_exam_stats(uqr)
    exam_stats_users = get_exam_stats(uqr_users)

    latest_exams = Exam.objects.all().order_by('pud_date')[:latest_n]

    template = loader.get_template("training/exams_page.html")
    context = {
        'exam_stats_overall_accuracy': exam_stats_overall['accuracy'][:top_n],
        'exam_stats_overall_popularity':
            exam_stats_overall['popularity'][:top_n],
        'exam_stats_users_accuracy': exam_stats_users['accuracy'][:top_n],
        'exam_stats_users_popularity': exam_stats_users['popularity'][:top_n],
        'top_n': top_n,
        'latest_exams': latest_exams[::-1],
        'latest_n': latest_n,
        'theme': get_theme(request)
    }

    return HttpResponse(template.render(context, request))


def exam(request, exam_id):
    """Exam view"""

    exam_object = Exam.objects.get(id=exam_id)

    template = loader.get_template("training/exam.html")
    context = {
        'name': exam_object.name,
        'description': exam_object.description,
        'theme': get_theme(request)
    }

    return HttpResponse(template.render(context, request))


def exam_content(request, exam_id):
    """Exam content view"""

    question_objects = Question.objects.filter(exam_id=exam_id)

    question_id_list = [question.id for question in question_objects]

    QuestionFormSet = formset_factory(
        form=QuestionForm,
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

                answer_correct = Answer.objects.get(
                    question=question_id, is_correct=True)
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
            'theme': get_theme(request)
        }

        return HttpResponse(template.render(context, request))


def exam_result(request, result_session_id):
    """Exam result view"""

    if request.method == 'POST':
        pass
    else:
        uqr_objects = UserQuestionResult.objects.filter(
            result_session=result_session_id)
        answers_info = {
            'question': [],
            'user_answer': [],
            'right_answer': [],
            'is_correct': []
        }
        answers_total = {
            'answers': [0],
            'right_answers': [0],
            'accuracy': []
        }
        for uqr in uqr_objects:
            right_answer_text = Answer.objects.get(
                question=uqr.question.id, is_correct=True).text
            answers_info['question'].append(uqr.question.text)
            answers_info['user_answer'].append(uqr.answer.text)
            answers_info['right_answer'].append(right_answer_text)
            answers_info['is_correct'].append(uqr.answer.is_correct)

            answers_total['answers'][0] += 1
            if uqr.answer.is_correct:
                answers_total['right_answers'][0] += 1

        answers_total['accuracy'].append(
            f'{round(
                100 * answers_total['right_answers'][0]
                / answers_total['answers'][0],
                2
            )}%'
        )

        df = pd.DataFrame.from_dict(answers_info)
        df_total = pd.DataFrame.from_dict(answers_total)

        template = loader.get_template("training/exam_result.html")
        context = {
            'df': df,
            'df_total': df_total,
            'exam_id': uqr_objects[0].exam.id,
            'theme': get_theme(request)
        }

        return HttpResponse(template.render(context, request))
