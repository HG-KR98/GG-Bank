from django.db import models

# Create your models here.
class Exchange(models.Model):
    cur_unit = models.CharField(max_length=100)
    ttb = models.FloatField()
    tts = models.FloatField()
    kftc_deal_bas_r = models.FloatField()