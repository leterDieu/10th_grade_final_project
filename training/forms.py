"""Forms"""


from logging import disable
from django import forms
from django.contrib.auth.models import User
from api.models import (
    Exam,
    Question,
    Answer,
    UserQuestionResult,
)
from django.forms import BaseFormSet


class QuestionForm(forms.Form):
    """One question form"""

    def __init__(self, *args, question_id, **kwargs):
        """Custom init to define answers
        depending on the question id"""

        super(QuestionForm, self).__init__(*args, **kwargs)

        answer_objects = Answer.objects.all()\
            .filter(question_id=question_id)

        answer_choices = [
            (i, answer.text) for i, answer in enumerate(answer_objects)
        ]

        self.fields['answer'] = forms.ChoiceField(
            widget=forms.RadioSelect(),
            choices=answer_choices,
            label=answer_objects[0].question.text
        )


class BaseQuestionFormSet(BaseFormSet):
    """Base formset for questions"""

    def get_form_kwargs(self, index):
        """Get form kwargs for a specific form in the formset"""
        kwargs = super(BaseQuestionFormSet, self).get_form_kwargs(index)
        question_id = kwargs['question_id_list'][index]
        return {'question_id': question_id}
