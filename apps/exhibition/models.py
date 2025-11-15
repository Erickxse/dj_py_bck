from django.db import models
from apps.stand.models import CexCountry
from apps.dashboard.fields import BitBooleanField

# Create your models here.
class CexExhibition(models.Model):
    stand_id = models.IntegerField()
    url_image = models.CharField(max_length=250)
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    code = models.TextField(blank=True, null=True)
    date_final = models.DateField(blank=True, null=True)
    slug = models.CharField(max_length=255)
    country = models.ForeignKey(CexCountry,  models.DO_NOTHING)
    
    class Meta:
        managed = False
        db_table = 'cex_exhibition'
        unique_together = (('slug', 'stand_id', 'country_id'),)
