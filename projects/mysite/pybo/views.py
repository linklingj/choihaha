from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, F, Count
from django.utils import timezone
from .models import Category, Question, Answer, Comment
from .forms import QuestionForm, AnswerForm, CommentForm
from .rank import hotRank


def index(request, category="all"):
	"""
	pybo 목록 출력
	"""
	page = request.GET.get('page', '1') #페이지
	kw = request.GET.get('kw', '') #검색어
	st = request.GET.get('st', '') #검색 타입
	so = request.GET.get('so', 'recent') #정렬 기준
	
	if category == "all":
		question_list = Question.objects.all().order_by('-create_date')
	else:
		c = get_object_or_404(Category, link_name=category)
		question_list = Question.objects.filter(Q(category=c)).order_by('-create_date')
	#question_list = Question.objects.all().order_by('-create_date')
	
	if so:
		if so == 'recent':
			question_list = question_list.order_by('-create_date')
		elif so == 'recommend':
			question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
		elif so == 'hot':
			question_list = question_list.annotate(rank=hotRank(Count('voter'),Count('down_voter'), Count('answer'))).order_by('-rank', '-create_date')

	if kw:
		if st == 'title':
			question_list = question_list.filter(Q(subject__icontains=kw)).distinct()
		elif st == 'title_and_content':
			question_list = question_list.filter(Q(subject__icontains=kw) | Q(content__icontains=kw)).distinct()
		elif st == 'author':
			question_list = question_list.filter(Q(author__username__icontains=kw)).distinct()

	paginator = Paginator(question_list, 20)
	page_obj = paginator.get_page(page)
	
	context = {'question_list': page_obj, 'page':page, 'kw':kw, 'so':so, 'cat':category}
	return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
	"""
	pybo 내용 출력
	"""
	question = get_object_or_404(Question, pk=question_id)
	
	context = {'question': question}
	
	return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_create(request, question_id):
	"""
	pybo 답변 등록
	"""
	question = get_object_or_404(Question, pk=question_id)
	if request.method == 'POST':
		form = AnswerForm(request.POST)
		if form.is_valid():
			answer = form.save(commit=False)
			answer.author = request.user
			answer.create_date = timezone.now()
			answer.question = question
			answer.save()
			return redirect('pybo:detail', question_id=question.id)
	else:
		form = AnswerForm()
	context = {'question': question, 'form': form}
	return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def question_create(request):
	"""
	pybo 질문 등록
	"""
	df = request.GET.get('df', 'anyquestion') #기본 카테고리
	# 카테고리 뷰에서 바로 작성했을때 기본 카테고리 설정 해주는 기능: 나중에 추가할것
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			question = form.save(commit=False)
			question.author = request.user
			question.create_date = timezone.now()
			category_name = form.cleaned_data['category']
			question.category = get_object_or_404(Category, name=category_name)
			question.save()
			return redirect('pybo:index')
	else:
		form = QuestionForm()
	categories = Category.objects.all()
	context = {'categories': categories, 'default': df, 'form': form}
	return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
	"""
	pybo 질문 수정
	"""
	question = get_object_or_404(Question, pk=question_id)
	if request.user != question.author:
		messages.error(request, '권한이 없습니다.')
		return redirect('pybo:detail', question_id=question.id)

	if request.method == 'POST':
		form = QuestionForm(request.POST, instance=question)
		if form.is_valid():
			question = form.save()
			question.author = request.user
			question.modify_date = timezone.now()
			category_name = form.cleaned_data['category']
			question.category = get_object_or_404(Category, name=category_name)
			question.save()
			return redirect('pybo:detail', question_id=question.id)
	else:
		form = QuestionForm(instance=question)
	categories = Category.objects.all()
	default = question.category.link_name
	context = {'categories': categories, 'default': default, 'form': form}
	return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
	"""
	pybo 질문 삭제
	"""
	question = get_object_or_404(Question, pk=question_id)
	if request.user != question.author:
		messages.error(request, '권한이 없습니다.')
		return redirect('pybo:detail', question_id=question.id)
	question.delete()
	return redirect('pybo:index')

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
	"""
	pybo 답변 삭제
	"""
	answer = get_object_or_404(Answer, pk=answer_id)
	if request.user != answer.author:
		messages.error(request, '권한이 없습니다.')
	else:
		answer.delete()
	return redirect('pybo:detail', question_id=answer.question_id)

@login_required(login_url='common:login')
def comment_create(request, answer_id):
	"""
	pybo 댓글 작성
	"""
	answer = get_object_or_404(Answer, pk=answer_id)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.author = request.user
			comment.create_date = timezone.now()
			comment.answer = answer
			comment.save()
			return redirect('pybo:detail', question_id=answer.question_id)
	else:
		form = CommentForm()
	context = {'form': form}
	return render(request, 'pybo/comment_form.html', context)
			

@login_required(login_url='common:login')
def comment_delete(request, comment_id):
	"""
	pybo 댓글 삭제
	"""
	comment = get_object_or_404(Comment, pk=comment_id)
	if request.user != comment.author:
		messages.error(request, '권한이 없습니다.')
	else:
		comment.delete()
	return redirect('pybo:detail', question_id=comment.answer.question_id)

@login_required(login_url='common:login')
def question_like(request, question_id):
	"""
	pybo 질문 좋아요
	"""
	question = get_object_or_404(Question, pk=question_id)
	if request.user == question.author:
		messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
	else:
		question.voter.add(request.user)
	return redirect('pybo:detail', question_id=question.id)
	
@login_required(login_url='common:login')
def answer_like(request, answer_id):
	"""
	pybo 답변 좋아요
	"""
	answer = get_object_or_404(Answer, pk=answer_id)
	if request.user == answer.author:
		messages.error(request, '본인이 작성한 댓글은 추천할 수 없습니다')
	else:
		answer.voter.add(request.user)
	return redirect('pybo:detail', question_id=answer.question_id)
	
@login_required(login_url='common:login')
def comment_like(request, comment_id):
	"""
	pybo 댓글 좋아요
	"""
	comment = get_object_or_404(Comment, pk=comment_id)
	if request.user == comment.author:
		messages.error(request, '본인이 작성한 댓글은 추천할 수 없습니다')
	else:
		comment.voter.add(request.user)
	return redirect('pybo:detail', question_id=comment.answer.question_id)
	
@login_required(login_url='common:login')
def question_dislike(request, question_id):
	"""
	pybo 질문 싫어요
	"""
	question = get_object_or_404(Question, pk=question_id)
	if request.user == question.author:
		messages.error(request, '본인이 작성한 글은 비추천할 수 없습니다')
	else:
		question.down_voter.add(request.user)
	return redirect('pybo:detail', question_id=question.id)
	
@login_required(login_url='common:login')
def answer_dislike(request, answer_id):
	"""
	pybo 답변 싫어요
	"""
	answer = get_object_or_404(Answer, pk=answer_id)
	if request.user == answer.author:
		messages.error(request, '본인이 작성한 댓글은 비추천할 수 없습니다')
	else:
		answer.down_voter.add(request.user)
	return redirect('pybo:detail', question_id=answer.question_id)
	
@login_required(login_url='common:login')
def comment_dislike(request, comment_id):
	"""
	pybo 댓글 싫어요
	"""
	comment = get_object_or_404(Comment, pk=comment_id)
	if request.user == comment.author:
		messages.error(request, '본인이 작성한 댓글은 비추천할 수 없습니다')
	else:
		comment.down_voter.add(request.user)
	return redirect('pybo:detail', question_id=comment.answer.question_id)
