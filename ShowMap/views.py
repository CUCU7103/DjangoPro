from django.shortcuts import render
import pickle
from .models import JejuFacility, JejuPop
import pandas as pd
import numpy as np
from django.http import HttpResponse
import math
import json
import os
    # 지도 보여주기 
def showmap(request):
    return render(request, "map.html")


#=================================================================
#  * @author jujuclubw
#  * @email dlrkdwn428@gmail.com
#  * @create date 2023-06-14 14:01:59
#  * @modify date 2023-06-14 14:01:59
#  * @desc [유클리디안 거리계산]
def uclid_process(data_merge,spot_data): #제주 시설 데이터, 위치 데이터 
    # 결과 데이터프레임 초기화
    result_data = pd.DataFrame(columns=['장소명', '자전거도로', '지하철역', '공원', '관광지','대학'])
    
    spot_data['위도'] = spot_data['위도'].astype(float)
    spot_data['경도'] = spot_data['경도'].astype(float)

    for spot_index, spot_row in spot_data.iterrows():
        spot_name = spot_row['장소명']
        spot_longitude = spot_row['경도']
        spot_latitude =  spot_row['위도']

        # 거리 계산을 위한 데이터프레임 복사 및 컬럼 추가
        temp_result = data_merge.copy()
        temp_result['최단거리'] = 0.0
        temp_result['장소명'] = spot_name
        #temp_result['총이동']=0

        #구 유동인구
        # imsi=0
        # for p in jeju_pop:
        #     if p.j_gu == spot_data.loc[spot_index,'장소명']:
        #         imsi=p.j_pop
        #         break
        # print('imsi2',imsi)

        # 유클리드 거리 계산
        temp_result['최단거리'] = np.sqrt(
            np.power(temp_result['경도'] - spot_longitude, 2) +
            np.power(temp_result['위도'] - spot_latitude, 2)
        )

        # 주제별 최단거리를 구하기 위해 그룹화하여 최소값 선택
        temp_result = temp_result.groupby(['장소명', '주제'])['최단거리'].min().reset_index()
        temp_result = temp_result.pivot(index='장소명', columns='주제', values='최단거리').reset_index()

        # 결과 데이터프레임에 추가
        result_data = pd.concat([result_data, temp_result], ignore_index=True)
        
    #  * @author jisu youn
    #  * @email yjs60130@gmail.com
    #  * @create date 2023-06-16 09:42:16
    #  * @modify date 2023-06-16 09:42:16
    #  * @desc 거리 조정
    result_data['자전거도로']=result_data['자전거도로']*1.15
    result_data['지하철역']=result_data['지하철역']*0.7
    result_data['공원']=result_data['공원']*0.55
    result_data['관광지']=result_data['관광지']*0.5
    result_data['대학']=result_data['대학']*0.45   
    
    return result_data

#  * @author jujuclubw
#  * @email dlrkdwn428@gmail.com
#  * @create date 2023-06-15 16:22:07
#  * @modify date 2023-06-15 16:22:07
#  * @desc [위경도 차이값 미터 변환함수]
def convert(latitude_diff, longitude_diff):
    latitude_meters = latitude_diff * 111111
    longitude_meters = longitude_diff * (math.cos(math.radians(latitude_diff)) * 111111)
    distance_in_meters = math.sqrt(latitude_meters**2 + longitude_meters**2)
    return round(distance_in_meters, 2)

#  * @author jujuclubw
#  * @email dlrkdwn428@gmail.com
#  * @create date 2023-06-14 11:46:55
#  * @modify date 2023-06-14 11:46:55
#  * @desc [제주 시설 검색]
def jeju_analysis(request):
    if request.method == 'POST':
        jeju_facility = list(JejuFacility.objects.all())
        
        #최단 검색용 제주 시설 df
        f_datas = []
        for j in jeju_facility:
            dic = {
                '장소명':j.j_name,
                '위도':j.j_latitude,
                '경도':j.j_longitude,
                '주제':j.j_theme,
                }
            f_datas.append(dic)
        jeju_facility_df = pd.DataFrame(f_datas)

        #선택한 제주 위경도
        ping = {
            '장소명':[request.POST['juso1'],request.POST['juso2'],request.POST['juso3']],
            '위도':[request.POST['lat1'],request.POST['lat2'],request.POST['lat3']],
            '경도':[request.POST['lng1'],request.POST['lng2'],request.POST['lng3']],
        }
        spot_data = pd.DataFrame(ping)
        spot_data.replace('', np.nan, inplace=True)
        spot_data.dropna(inplace=True)
        
        result_data = uclid_process(jeju_facility_df,spot_data)
        # 컬럼에 함수 적용하여 결과 저장

        #모델예측
        # '장소명' 컬럼을 제외한 값 선택
        X = result_data.drop(columns=['장소명'])
        
        # # 모델 로드
        # import joblib
        # model = joblib.load('static/model/MLP.pkl') 
       
        # pkl 파일 경로
        #pkl_file_path = "static/model/knn_model_5_stdX.h5"
        # print(os.getcwd())
        pkl_file_path = "ShowMap/static/model/knn_model_5_stdX.h5"
        import pickle
        # pkl 파일 로드
        with open(pkl_file_path, 'rb') as file:
            model = pickle.load(file)
            
        # 예측 수행
        y_pred = model.predict(X)
        df_pred = pd.DataFrame({'예측값': y_pred})

        df_result = pd.concat([result_data['장소명'],X, df_pred], axis=1)
        # 출력전 위경도 간 데이터 미터로 변환
        df_result['자전거도로'] = result_data.apply(lambda row: convert(row['자전거도로'], row['자전거도로']), axis=1)
        df_result['지하철역'] = result_data.apply(lambda row: convert(row['지하철역'], row['지하철역']), axis=1)
        df_result['공원'] = result_data.apply(lambda row: convert(row['공원'], row['공원']), axis=1)
        df_result['관광지'] = result_data.apply(lambda row: convert(row['관광지'], row['관광지']), axis=1)
        df_result['대학'] = result_data.apply(lambda row: convert(row['대학'], row['대학']), axis=1)
        
        #서울시 최대거리 기준으로 점수화
        #print('공원',convert(0.03433583,0.03433583),'관광지',convert(0.07511377,0.07511377),'대학',convert(0.08019374,0.08019374))
        #공원 5395.35 관광지 11802.97 대학 12601.21
        
        df_result['자전거도로']=100-(df_result['자전거도로']/13400*100)
        df_result['지하철역']=100-(df_result['지하철역']/7500*100)
        df_result['공원']=100-(df_result['공원']/6000*100)
        df_result['관광지']=100-(df_result['관광지']/10500*100)
        df_result['대학']=100-(df_result['대학']/12000*100) 
        
        df_result.loc[df_result['자전거도로'] < 0] = 0
        df_result.loc[df_result['지하철역'] < 0, '지하철역'] = 0
        df_result.loc[df_result['공원'] < 0, '공원'] = 0
        df_result.loc[df_result['관광지'] < 0, '관광지'] = 0
        df_result.loc[df_result['대학'] < 0, '대학'] = 0

        df_result=df_result.round(2)
        
        df_result['장소명']=df_result['장소명'].astype(str).str.replace(' ', '_')
        
        #print(df_result['장소명'])

        return render(request,"mainresult.html",{'result':df_result})
    
    if request.method == 'GET':
        #  * @author jujuclubw
        #  * @email dlrkdwn428@gmail.com
        #  * @create date 2023-06-15 11:28:17
        #  * @modify date 2023-06-15 11:28:17
        #  * @desc [차트출력]
        dic = {
            'place':request.GET['place'],
            'cycle':request.GET['cycle'],
            'train':request.GET['train'],
            'park':request.GET['park'],
            'tour':request.GET['tour'],
            'school':request.GET['school'],
            'pop':request.GET['pop']}
        #print(dic)
        return HttpResponse(json.dumps(dic), content_type="application/json")
