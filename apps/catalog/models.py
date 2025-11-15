from django.db import models

class CexCatalog(models.Model):
    stand_id = models.IntegerField()
    category_id = models.IntegerField(blank=True, null=True)
    seo_id = models.IntegerField()
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    img_pdf = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=150, blank=True, null=True)
    hits = models.IntegerField(blank=True, null=True)
    slug = models.CharField(unique=True, max_length=255)
    country_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cex_catalog'
