from django.shortcuts import render
from .models import JejuFacility
import pandas as pd
import numpy as np
from django.http import HttpResponse
import json 
from sklearn.preprocessing import StandardScaler
    # 지도 보여주기 
def showmap(request):
    return render(request, "map.html")

#  * @author jujuclubw
#  * @email dlrkdwn428@gmail.com
#  * @create date 2023-06-14 14:01:59
#  * @modify date 2023-06-14 14:01:59
#  * @desc [description]
def uclid_process(data_merge,spot_data):
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
        result_data['자전거도로']=result_data['자전거도로']*1.05
        result_data['지하철역']=result_data['지하철역']*0.85
        result_data['공원']=result_data['공원']*0.65
        result_data['관광지']=result_data['관광지']*0.7
        result_data['대학']=result_data['대학']*0.70
        result_data['총이동']=0
    return result_data

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

        #모델예측
        # '장소명' 컬럼을 제외한 값 선택
        X = result_data.drop(columns=['장소명'])
        # 데이터 표준화
        # scaler = StandardScaler()
        # X_scaled = scaler.fit_transform(X)
        # pkl 파일 경로
        pkl_file_path = "static/model/knn_model_6_stdX.h5"
        import pickle
        # pkl 파일 로드
        with open(pkl_file_path, 'rb') as file:
            model = pickle.load(file)
        
        # 모델 로드
        import joblib
        model = joblib.load('static/model/MLP.pkl') 
        # 예측 수행
        y_pred = model.predict(X)
        df_pred = pd.DataFrame({'예측값': y_pred})

        df_result = pd.concat([result_data['장소명'],X, df_pred], axis=1)
        print(df_result)
    
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
            'school':request.GET['school']}
        return HttpResponse(json.dumps(dic), content_type="application/json")
        
        
