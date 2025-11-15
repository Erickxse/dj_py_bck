from django.db import models

# Create your models here.
class CexCategory(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True, null=True, db_comment='Descripci≤n corta para SEO')
    description = models.TextField(blank=True, null=True)
    img = models.CharField(max_length=100, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    level = models.IntegerField()
    slug = models.CharField(unique=True, max_length=255)
    type = models.CharField(max_length=20, db_comment='producto ½product╗ o servicio ½service╗')
    credits = models.FloatField(blank=True, null=True, db_comment='Creitos solo para terce nivel')
    def_type = models.CharField(max_length=5)
    def_price = models.FloatField()
    do_related = models.TextField()  # This field type is a guess.
    coins_coefficient = models.FloatField(blank=True, null=True)
    min_coins = models.IntegerField(blank=True, null=True)
    max_coins = models.IntegerField(blank=True, null=True)
    industry_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cex_category'