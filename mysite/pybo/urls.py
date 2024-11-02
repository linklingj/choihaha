from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
	path('', views.index, name='index'),
	path('<str:category>/', views.index, name='index'),
	path('question/<int:question_id>/', views.detail, name='detail'),
	path('question/create/', views.question_create, name='question_create'),
	path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
	path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
	path('question/like/<int:question_id>/', views.question_like, name='question_like'),
	path('question/dislike/<int:question_id>/', views.question_dislike, name='question_dislike'),
	path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
	path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
	path('answer/like/<int:answer_id>/', views.answer_like, name='answer_like'),
	path('answer/dislike/<int:answer_id>/', views.answer_dislike, name='answer_dislike'),
	path('comment/create/<int:answer_id>/', views.comment_create, name='comment_create'),
	path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
	path('comment/like/<int:comment_id>/', views.comment_like, name='comment_like'),
	path('comment/dislike/<int:comment_id>/', views.comment_dislike, name='comment_dislike'),
]