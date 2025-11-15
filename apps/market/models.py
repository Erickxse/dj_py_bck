from django.db import models

# Create your models here.


class CexLandingPages(models.Model):
    seo_title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    seo_description = models.CharField(max_length=255)
    front_block = models.TextField(blank=True, null=True)
    seo_keywords = models.CharField(max_length=255)
    has_slider_revolution = models.IntegerField()
    slider_revolution_file = models.CharField(max_length=255)
    slider_revolution_date = models.DateTimeField(blank=True, null=True)
    slider_id = models.IntegerField(blank=True, null=True)
    tour_switch = models.IntegerField()
    tour_virtual_code = models.TextField(blank=True, null=True)
    foot_bar = models.IntegerField()
    image_url = models.CharField(max_length=255, blank=True, null=True)
    promo_title = models.TextField(blank=True, null=True)
    spaces_public = models.IntegerField()
    is_public = models.IntegerField()
    adsense_enabled = models.IntegerField()
    adsense_code = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cex_landing_pages'
