from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse

from ..forms import CommentForm
from ..models import Question , Answer, Comment

@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = CommentForm(request.POST) # 저장하기를 하면 POST 방식으로 요청
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user # author 속성에 로그인 계정 저장
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            #댓글 작성하고 댓글 작성했던 질문으로 돌아가기
            return redirect(f"{reverse('pybo:detail', kwargs={'question_id': question.id})}#comment_{comment.id}")
    else:
        form = CommentForm()
    context = {'form': form, 'question': question} 
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST':
        form = CommentForm(request.POST) # 저장하기를 하면 POST 방식으로 요청
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user # author 속성에 로그인 계정 저장
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            #댓글 작성하고 댓글 작성했던 답변으로 돌아가기
            return redirect(f"{reverse('pybo:detail', kwargs={'question_id': answer.question.id})}#comment_{comment.id}")
    else:
        form = CommentForm()
    context = {'form': form, 'answer': answer} 
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.question.id if comment.question else comment.answer.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect(f"{reverse('pybo:detail', kwargs={'question_id': comment.question.id if comment.question else comment.answer.question.id})}#comment_{comment.id}")
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제 권한이 없습니다.')
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question.id if comment.question else comment.answer.question.id)
