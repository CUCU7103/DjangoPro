from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

# Create your views here.
def homeFunc(request):
    return render(request, "home.html")

#test 230610 jujuclubw

# 로그인 관련 로직 작성 진행함. 
# 23.06.12
def login(request):
    return render(request, "account.html")
        
