# /**
#  * @author jujuclubw
#  * @email dlrkdwn428@gmail.com
#  * @create date 2023-06-13 11:11:22
#  * @modify date 2023-06-13 11:11:22
#  * @desc ShowStat 통계페이지 앱 생성
#  */
from django.shortcuts import render


def showstat(request):
    return render(request,"statistic.html")