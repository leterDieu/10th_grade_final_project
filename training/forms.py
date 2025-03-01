from django import forms
from django.contrib.auth.models import User
from api.models import (
    Exam,
    Question,
    Answer,
    UserQuestionResult
)


class QuestionForm(forms.Form):
    def __init__(self, question_id, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        answer_objects = Answer.objects.all()\
        .filter(question_id=question_id)

        answer_choices = [(i, answer.text) for i, answer in enumerate(answer_objects)]

        self.fields['answer'] = forms.ChoiceField(
            widget=forms.RadioSelect(),
            choices=answer_choices,
            label=answer_objects[0].question.text
        )
