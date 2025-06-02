from django.contrib.auth import authenticate, login, logout #django.contrib.auth의 logout 함수를 이용
from django.shortcuts import render, redirect
from common.forms import UserForm

def logout_view(request):
    logout(request)
    return redirect('index') #index 페이지로 리다이렉트

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})