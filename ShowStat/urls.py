    # /**
    #  * @author jujuclubw
    #  * @email dlrkdwn428@gmail.com
    #  * @create date 2023-06-13 11:12:01
    #  * @modify date 2023-06-13 11:12:01
    #  * @desc 통계 메인 url.py 생성
    #  */
from django.urls import path
from . import views

urlpatterns = [
    path("", views.showstat),

]