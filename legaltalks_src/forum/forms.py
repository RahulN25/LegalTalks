from django import forms
from .models import Question, Answer
from django.conf import settings

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = (
            'is_anonymous',
            'category',
            'question_title',
            'question_body',
        )

    def save(self, usr=None, commit=True, *args, **kwargs):
        question = super().save(commit=False)
        if usr is not None:
            question.author = usr
        if commit:
            question.save()
        return question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = (
            'is_anonymous',
            'answer_body'
        )

    def save(self, usr=None, ques=None, commit=True, *args, **kwargs):
        answer = super().save(commit=False)
        if usr is not None:
            answer.answerer = usr
        if ques is not None:
            answer.answer_for = ques
        if commit:
            answer.save()
        return answer