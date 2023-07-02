from django.shortcuts import render
import folium
import pandas as pd
import json
from django.http import JsonResponse
from folium.plugins import MarkerCluster
import numpy as np
import matplotlib.pyplot as plt
from folium import plugins

# Create your views here.
def index(request):
    return render(request,'index.html')
def login(request):
    return render(request,'login.html')
def register(request):
    return render(request,"register.html")
def err(request):
    return render(request,"404.html")
def card(request):
    return render(request,"cards.html")
def forgotpw(request):
    return render(request,"forgot-password.html")

def charts(request):
    
    df = pd.read_excel("./rental3.xlsx") #칼럼: 지역번호, 지역구, 대여소갯수
    
    # 지도의 기준이 되는 위도 경도 
    # 서울의 위도 경도이다.
    latitude = 37.562225
    longitude = 126.978555
    
    # 지도 객체 생성
    m  = folium.Map(
        location= [latitude, longitude],
        zoom_start=10, # 줌
        tiles= "OpenStreetMap",
    )
    
    # with open()문을 사용하면 with문을 벗어날 떄 자동으로 파일이 닫힘
    with open('./hangjeongdong_.json',mode='rt',encoding='utf-8') as f: #f는 파일 객체
        geo = json.loads(f.read())    
    #파일을 열고 작업을 수행하는 동안에는 파일에 대한 자원(메모리, 파일 핸들 등)이 할당되고 락이 설정됨
    #파일을 닫으면 이러한 자원을 해제해 다른 프로세스나 스레드에서 접근 가능해짐
    
    #[GeoJSON]
    #지리 정보(Geographic Information)를 표현하기 위한 개방형 표준 데이터 형식
    #JSON(JavaScript Object Notation) 형식을 기반으로 하며, 지리 데이터를 구조화하여 저장하고 전송하기 위해 설계됨
    # 개체타입
    # 1. Feature (특징): 지리적인 개체 하나를 나타내는 개체
    # 2. Feature Collection (특징 컬렉션): 여러 개의 Feature를 그룹화한 컬렉션입니다. 한 GeoJSON 파일에 여러 개의 Feature를 포함할 때 사용
    # 3. Geometry (지오메트리): 지리 개체의 형태를 정의하는 객체로, 점(Point), 선(LineString), 다각형(Polygon) 등의 지오메트리 타입이 있습니다.
    # 4. Properties (속성): Feature나 Feature Collection에 대한 추가 정보를 저장하는 객체
    
    folium.Choropleth(
        geo_data= geo,
        name='choropleth',
        data=df, 
        columns=['지역번호','대여소갯수'], # 데이터프레임의 컬럼들
        key_on='feature.properties.code', # geojson 피처의 키
        fill_color='Reds',
        fill_opacity=0.7,
        line_opacity=0.7,
        color = 'black',
        overlay="True",
        legend_name='대여소 분포',
    ).add_to(m) #Choropleth 레이어를 지도 m에 추가
    
    maps1 = m._repr_html_() #지도 m을 HTML 형식으로 변환
    
    # 서울시 지자체별 파일
    # state_geo = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'

    # 서울시 유동인구 파일(행정구역별,나이대별,총이동)
    df = pd.read_csv('./seoul_float_pop_age.csv',encoding='utf-8')
    p=df[['행정구역별','총이동']]

    # 지도 생성함    
    elec_district_geo_map = folium.Map(location=[latitude, longitude], tiles="OpenStreetMap", zoom_start=10)
    
    # 시각화 
    folium.Choropleth(
        geo_data=geo,
        name='자치구 별 유동인구',
        data=p,
        columns=('행정구역별','총이동'),
        key_on='feature.properties.name',
        fill_color='Reds',
        fill_opacity = 0.7,
        line_opacity = 0.7,
        color = 'black',
        legend_name = '유동인구 수'
    ).add_to(elec_district_geo_map)

    maps2 = elec_district_geo_map._repr_html_()

#--------------------------------------------------------------------

    df = pd.read_csv('./rental.csv',encoding='cp949') #서울시 대여소. 컬럼: 대여소_ID,주소1,주소2,위도,경도
    df1 = df[(df['위도'] != 0) & (df['경도'] != 0)]
    df = df1.reset_index(drop=True)
    sub = df[['위도','경도']]
    # print(sub)
    
    # # 서울시 위도
    # latitude = 37.541
    # # 서울시 경도
    # longitude = 126.986
    
    # 지도 생성
    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=10,
    )
    
    coords = sub
    # marker cluster 객체를 생성
    datas = zip(coords['위도'], coords['경도']) #데이터프레임의 '위도'와 '경도' 컬럼 값을 묶어서 datas라는 이터러블 객체(zip 객체)로 생성
    plugins.FastMarkerCluster(data=datas).add_to(m) #FastMarkerCluster 클러스터를 지도 객체(m)에 추가
   
    
    # 데이터의 위도, 경도를 받아서 마커를 생성함.
    # for lat, long in zip(coords['위도'], coords['경도']):
    #     folium.Marker([lat, long], icon = folium.Icon(color="green")).add_to(marker_cluster)
    
    # 템플릿에 보내기 위해서 사용함.
    maps3 = m._repr_html_()
    
    
    # 제주도 자전거 데이터
    
    df = pd.read_csv('./rentaljeju.csv', encoding='cp949')
    sub2 = df[['위도','경도']]
    # print(sub2)
    
    # 제주도 위도
    latitude1 = 33.499
    # 제주시 경도
    longitude1 = 126.531
    
    # 지도 생성
    m2 = folium.Map(
        location=[latitude1, longitude1],
        zoom_start=10,
    )
    
    coords = sub2
    # marker cluster 객채를 생성
    datas = zip(coords['위도'], coords['경도'])
    plugins.FastMarkerCluster(data=datas).add_to(m2)
    
    
    # 데이터의 위도, 경도를 받아서 마커를 생성함.
    # for lat, long in zip(coords['위도'], coords['경도']):
    #     folium.Marker([lat, long], icon = folium.Icon(color="green")).add_to(marker_cluster)
    
    # 템플릿에 보내기 위해서 사용함.
    maps4 = m2._repr_html_()
    

    return render(request,"charts.html",{"maps1":maps1,"maps2":maps2,"maps3":maps3,"maps4":maps4})

