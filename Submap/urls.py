from django.urls import path
from . import views



urlpatterns = [
    path("submap/", views.rental),
    path("chart/", views.chart),
    
]

