from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)
	link_name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.name

class Question(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
	subject = models.CharField(max_length = 200)
	content = models.TextField()
	create_date = models.DateTimeField(auto_now_add = True)
	modify_date = models.DateTimeField(null=True, blank=True)
	voter = models.ManyToManyField(User, related_name='voter_question')
	down_voter = models.ManyToManyField(User, related_name='down_voter_question')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')

	def __str__(self):
		return self.subject

class Answer(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
	question = models.ForeignKey(Question, on_delete = models.CASCADE)
	content = models.TextField()
	create_date = models.DateTimeField(auto_now_add = True)
	modify_date = models.DateTimeField(null=True, blank=True)
	voter = models.ManyToManyField(User, related_name='voter_answer')
	down_voter = models.ManyToManyField(User, related_name='down_voter_answer')

class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	answer = models.ForeignKey(Answer, null=True, blank=True, on_delete = models.CASCADE)
	content = models.TextField()
	create_date = models.DateTimeField()
	modify_date = models.DateTimeField(null=True, blank=True)
	voter = models.ManyToManyField(User, related_name='voter_comment')
	down_voter = models.ManyToManyField(User, related_name='down_voter_comment')