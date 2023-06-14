from django.shortcuts import redirect, HttpResponse, HttpResponseRedirect, render
from django.http import JsonResponse
import json
import folium
from folium.plugins import MarkerCluster,FastMarkerCluster
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create your views here.
# 현재 서울시 자전거 대여소 현황 출력
def rental(request):
    df = pd.read_csv('../rental.csv',encoding='cp949')
    sub = df[['위도','경도']]
    # print(sub)
    
    # 서울시 위도
    latitude = 37.541
    # 서울시 경도
    longitude = 126.986
    
    # 지도 생성
    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=10,
    
    )
    
    coords = sub
    # marker cluster 객채를 생성
    marker_cluster = MarkerCluster().add_to(m)
   
    
    # 데이터의 위도, 경도를 받아서 마커를 생성함.
    for lat, long in zip(coords['위도'], coords['경도']):
        folium.Marker([lat, long], icon = folium.Icon(color="green")).add_to(marker_cluster)
    
    # 템플릿에 보내기 위해서 사용함.
    maps = m._repr_html_()
    
    # 제주도 자전거 데이터
    
    df = pd.read_csv('../rentaljeju.csv', encoding='cp949')
    sub2 = df[['위도','경도']]
    # print(sub2)
    
    # 제주도 위도
    latitude = 33.499
    # 서울시 경도
    longitude = 126.531
    
    # 지도 생성
    m2 = folium.Map(
        location=[latitude, longitude],
        zoom_start=10,
    )
    
    coords = sub2
    # marker cluster 객채를 생성
    marker_cluster = MarkerCluster().add_to(m2)
    
    # 데이터의 위도, 경도를 받아서 마커를 생성함.
    for lat, long in zip(coords['위도'], coords['경도']):
        folium.Marker([lat, long], icon = folium.Icon(color="green")).add_to(marker_cluster)
    
    # 템플릿에 보내기 위해서 사용함.
    map2 = m2._repr_html_() 
   
      
    return render(request,'submap.html',{'map':maps,'map2':map2})


# chart.js
def chart(request):
    
    # 데이터프레임을 JSon으로 변환
    df = pd.read_csv("../rentalnumber.csv", encoding="cp949")
    chartdata = df.to_json(orient='records',force_ascii=False)  
    chartdata = json.dumps(chartdata) # 디코딩
    chartdata = json.loads(chartdata) # 인코딩
    
    context= {'chartdata':chartdata}
    
    return render(request,"chart.html", context) # Json 데이터 전달함.
