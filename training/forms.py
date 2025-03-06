from logging import disable
from django import forms
from django.contrib.auth.models import User
from api.models import (
    Exam,
    Question,
    Answer,
    UserQuestionResult
)
from django.forms import BaseFormSet


class QuestionForm(forms.Form):
    def __init__(self, *args, question_id, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        answer_objects = Answer.objects.all()\
        .filter(question_id=question_id)

        answer_choices = [(i, answer.text) for i, answer in enumerate(answer_objects)]

        self.fields['answer'] = forms.ChoiceField(
            widget=forms.RadioSelect(),
            choices=answer_choices,
            label=answer_objects[0].question.text
        )


class BaseQuestionFormSet(BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super(BaseQuestionFormSet, self).get_form_kwargs(index)
        question_id = kwargs['question_id_list'][index]
        return {'question_id': question_id}
