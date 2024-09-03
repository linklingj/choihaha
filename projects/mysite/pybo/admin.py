from django.contrib import admin
from .models import Question, Answer, Comment, Category

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
	search_fields = ['subject']
class AnswerAdmin(admin.ModelAdmin):
	search_fields = ['author']
class CommentAdmin(admin.ModelAdmin):
	search_fields = ['author']
class CategoryAdmin(admin.ModelAdmin):
	search_fields = ['name']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)