# import django.contrib.auth
# from django.contrib.auth import authenticate, login
# from django.shortcuts import redirect
# from Login.forms import UserForm
from django.shortcuts import render,redirect
from django.contrib.sessions.models import Session
from . models import Member


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        m_id = request.POST.get('account')
        m_pwd = request.POST.get('password')
        errMsg = {}
        context= {}
        if not (m_id and m_pwd):
            errMsg["err"] = "모든 값을 입력하세요"
            
        else:
            user = Member.objects.get(m_id=m_id)
            print('m_pwd :', m_pwd)
            print('user.m_pwd :', user.m_pwd)
            if (m_pwd == user.m_pwd ):
                request.session['user'] = user.m_id
                
                print('로그인 성공')
                return redirect('/') # 로그인 성공시 홈으로 이동함.
            else:
                errMsg['error'] = "비밀번호를 입력하세요"
                print('로그인 실패')
        print('ㅎㅎㅎㅎㅎㅎ')
        return render(request, "login.html", errMsg)
                 
                   
                 
# 회원가입기능 구현 중
def signup(request): 
    if request.method =="GET":
        return render(request,'login.html')
    elif request.method == "POST": 
        m_id = request.POST.get('account')
        m_name = request.POST.get('username') 
        m_pwd = request.POST.get('password')  
        m_email = request.POST.get('email')
        
        res_data = {}
        
        if not (m_id and m_pwd):
            res_data["error"] = "모든 값을 입력해야 합니다."
        else:
            user = Member(m_id = m_id, m_name=m_name ,m_pwd = m_pwd, m_email = m_email)
            user.save()
        return redirect("/login")

# 로그아웃
def logout(request):
    del(request.session['user'])
    return redirect("/")


# Create your views here.
# authenticate() django의 인증기능
# def signup(request):
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid(): # 데이터 유효성 검사
#             form.save() 
#             username = form.cleaned_data.get("username") # cleaned_data 는 Form 의 안에서 정의한 필드에 값에 대해서만 리턴
#             raw_password = form.cleaned_data.get("password")
#             user = authenticate(username=username, password=raw_password)  # 사용자 인증
#             login(request,user) # 로그인 기능
#             return redirect('home')
            
#         else:
#             form = UserForm()
#         return render(request, 'signup.html', {'form':form})       
