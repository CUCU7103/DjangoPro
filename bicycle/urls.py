"""
URL configuration for bicycle project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from bicycleapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.homeFunc),
    path("login/", views.login), # 로그인 페이지
    path("showmap/", include('ShowMap.urls')), # 메인페이지 지도 보여줌
    path("report/", include("Report.urls")), # app name = Report의 url
]