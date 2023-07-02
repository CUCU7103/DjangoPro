# /**
#  * @author jujuclubw
#  * @email dlrkdwn428@gmail.com
#  * @create date 2023-06-13 11:11:22
#  * @modify date 2023-06-13 11:11:22
#  * @desc ShowStat 통계페이지 앱 생성
#  */
from django.shortcuts import redirect, HttpResponse, HttpResponseRedirect, render
from django.http import JsonResponse
import json
# import folium
# from folium.plugins import MarkerCluster
# from folium.plugins import MarkerCluster,FastMarkerCluster
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from django.http import JsonResponse

# def showstat(request):
#     df2 = pd.read_csv("월별이용건수.csv", encoding="UTF-8")
#     chartdata2 = df2.to_json(orient='records',force_ascii=False)  
#     chartdata2 = json.dumps(chartdata2) # 디코딩
#     chartdata2 = json.loads(chartdata2) # 인코딩

#     df3 = pd.read_csv("월별 신규가입자수.csv", encoding="UTF-8")
#     chartdata3 = df3.to_json(orient='records',force_ascii=False)  
#     chartdata3 = json.dumps(chartdata3) # 디코딩
#     chartdata3 = json.loads(chartdata3) # 인코딩
    
#     df4 = pd.read_csv("연도별 제주관광객수.csv", encoding="UTF-8")
#     chartdata4 = df4.to_json(orient='records',force_ascii=False)  
#     # chartdata = json.dumps(chartdata, ensure_ascii=False)
#     chartdata4 = json.dumps(chartdata4) # 디코딩
#     chartdata4 = json.loads(chartdata4) # 인코딩



#     context= {'chartdata2':chartdata2,'chartdata3':chartdata3,'chartdata4':chartdata4}
#     # return render(request,"statistic.html", context)

    
#     df = pd.read_excel("./rental3.xlsx")
#     # df = pd.read_csv('./rental3.csv',encoding="cp949")
#     # df['대여소_ID'] = range(0, 3225)
#     # df.set_index("시군구")
#     # index_list = []
#     # for index in range(0, 3224):
#     #     index_list.append(index)
#     # return index_list
        
        
#     # 값 확인 진행함.
#     # df['대여소_ID'] = df['대여소_ID'].replace(index_list)
#     # print(df.head())
#     # print(df.info())
#     # print(df.isnull())
    
#     # 지도의 기준이 되는 위도 경도 
#     # 서울의 위도 경도이다.
#     latitude = 37.562225
#     longitude = 126.978555
    
#     # 지도 생성함
#     m  = folium.Map(
#         location= [latitude, longitude],
#         zoom_start=10, # 줌
#         tiles= "OpenStreetMap",
#     )
    
#     # geojsondata
   
#     with open('./hangjeongdong_.json',mode='rt',encoding='utf-8') as f:
#         geo = json.loads(f.read())    
    
#     for feature in geo['features']:
#         code = feature['properties']['code']
#         name = feature['properties']['name']
#         print(code) 
#         print(name)
#         f.close()
    
#     # folium.GeoJson(
#     #     geo,
#     #     name='seoul_municipalities'
#     #     ).add_to(m)
    
    
#     folium.Choropleth(
#         geo_data= geo,
#         name='choropleth',
#         data=df, 
#         columns=['지역번호','대여소갯수'], # 데이터프레임의 컬럼들
#         key_on='feature.properties.code', # geojson 피처의 키
#         fill_color='YlGn',
#         fill_opacity=0.7,
#         line_opacity=0.7,
#         color = 'black',
#         legend_name='대여소 분포',
#     ).add_to(m)
    
#     maps1 = m._repr_html_()
    
#         # 서울시 지자체별 파일("code":"11250","name":"강동구","name_eng":"Gangdong-gu","base_year":"2013"},"geometry":{"type":"Polygon","coordinates":)
#     state_geo = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'
#     # 서울시 유동인구 파일(행정구역별,나이대별,총이동)
#     df = pd.read_csv('./seoul_float_pop_age.csv',encoding='utf-8')
#     p=df[['행정구역별','총이동']]
#     # 서울시 위도
#     # latitude = 37.541
#     # 서울시 경도
#     # longitude = 126.986

#     # 지도 생성함    
#     elec_district_geo_map = folium.Map(location=[latitude, longitude], tiles="OpenStreetMap", zoom_start=10)
    
#     # 시각화 
#     folium.Choropleth(
#         geo_data=state_geo,
#         name='자치구 별 유동인구',
#         data=p,
#         columns=('행정구역별','총이동'),
#         key_on='feature.properties.name',
#         fill_color='Greens',
#         fill_opacity = 0.7,
#         line_opacity = 0.7,
#         color = 'black',
#         legend_name = '유동인구 수'
#     ).add_to(elec_district_geo_map)

#     maps2 = elec_district_geo_map._repr_html_()

    
    
#     return render(request,"statistic.html",{"maps1":maps1,"maps2":maps2,
#                                             'chartdata2':chartdata2,'chartdata3':chartdata3,'chartdata4':chartdata4})



def showstat2(request):
    df2 = pd.read_csv("ShowStat/static/월별이용건수.csv", encoding="UTF-8")
    chartdata2 = df2.to_json(orient='records',force_ascii=False)  
    #print(type(chartdata2)) #<class 'str'>
    # JSON 형태(str)로 변환
    # orient 옵션을 'records'로 설정하면 각 행이 개별적인 JSON 객체로 구성되며, 
    # #force_ascii=False로 설정하면 유니코드 문자가 그대로 유지

    df3 = pd.read_csv("ShowStat/static/월별 신규가입자수.csv", encoding="UTF-8")
    chartdata3 = df3.to_json(orient='records',force_ascii=False)  
    
    df4 = pd.read_csv("ShowStat/static/연도별 제주관광객수.csv", encoding="UTF-8")
    chartdata4 = df4.to_json(orient='records',force_ascii=False)  

    return render(request,"charts2.html",{'chartdata2':chartdata2 ,'chartdata3':chartdata3,'chartdata4':chartdata4})










