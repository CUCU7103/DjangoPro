from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "Login"
urlpatterns = [
  # 로그인 기능
  path('',views.login), # 수정해야하는 코드
  # django.contrib.auth앱의 LoginView 클래스를 활용했으므로 별도의 views.py 파일 수정이 필요 없음
  
  # 로그아웃 기능
  path('logout/',views.logout),
  
  # 회원가입 기능
  path('signup/',views.signup, name='signup')
]