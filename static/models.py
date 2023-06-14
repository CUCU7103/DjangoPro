from django.db import models

# /**
#  * @author jujuclubw
#  * @email dlrkdwn428@gmail.com
#  * @create date 2023-06-14 10:23:13
#  * @modify date 2023-06-14 10:23:13
#  * @desc 제주 검색용 DB model추가
#  */
class JejuFacility(models.Model):
    j_name = models.CharField(max_length=50, blank=True, null=True)
    j_latitude = models.FloatField(blank=True, null=True)
    j_longitude = models.FloatField(blank=True, null=True)
    j_theme = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jeju_facility'