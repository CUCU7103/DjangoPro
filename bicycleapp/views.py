from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

# Create your views here.
def homeFunc(request):
    return render(request, "home.html")

# 로그아웃
def logout(request):
    del(request.session['user'])
    return redirect("/")

# test 230610 jujuclubw

# 로그인 관련 로직 작성 진행함. 로그인 app 신규생성함(06.13)

# # 23.06.12
# def login(request):
#     return render(request, "account.html")
   
