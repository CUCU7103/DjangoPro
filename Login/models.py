from django.db import models

# Create your models here.
class Member(models.Model):
    m_name = models.CharField(max_length=100)
    m_id = models.CharField(max_length=100)
    m_pwd = models.CharField(max_length=100)
    m_email = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'member'
