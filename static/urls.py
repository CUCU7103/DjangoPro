from django.urls import path
from . import views

urlpatterns = [
    path("map/", views.showmap),
    path("analysis",views.jeju_analysis)
]