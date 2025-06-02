from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.db import models

from ..forms import QuestionForm
from ..forms import AnswerForm
from ..models import Question

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST) # 저장하기를 하면 POST 방식으로 요청
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm() #질문 등록을 할 때는 GET 방식으로 요청
    context = {'form': form} 
    return render(request, 'pybo/question_form.html', context)

    
@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST": # 저장하기 버튼을 누르면 POST 방식으로 호출
        form = QuestionForm(request.POST, instance=question) #저장하기를 누르면 QuestionForm을 생성하지만 request.POST 값으로 덮어씌워라
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question) #inscance 값을 지정하면 폼의 속성값이 채워짐
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')


@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)


def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # 답변 페이징 처리
    answer_list = question.answer_set.all().annotate(
        num_votes=models.Count('voter')
    ).order_by('-num_votes','-create_date')
    page = request.GET.get('page', '1')
    paginator = Paginator(answer_list, 10)
    page_obj = paginator.get_page(page)

    form = AnswerForm()
    context = {
        'question': question,
        'page_obj': page_obj,
        'form': form
    }
    return render(request, 'pybo/question_detail.html', context)
