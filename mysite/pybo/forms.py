from django import forms
from pybo.models import Question, Answer, Comment, Category
from django.contrib.auth.models import User

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['subject', 'content', 'category']

	category = forms.ModelChoiceField(
		queryset=Category.objects.all(),
		to_field_name='link_name',
		required=True
	)

class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['content']

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']