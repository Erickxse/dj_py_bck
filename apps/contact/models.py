from django.db import models

class CexInbox(models.Model):
    name = models.CharField(max_length=80, blank=True, null=True)
    phone = models.CharField(max_length=80, blank=True, null=True)
    email = models.CharField(max_length=120, blank=True, null=True)
    organization = models.CharField(max_length=80, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=45)
    from_field = models.CharField(db_column='from', max_length=120, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    to = models.CharField(max_length=120, blank=True, null=True)
    stand_name = models.CharField(max_length=120, blank=True, null=True)
    mailed_it = models.DateTimeField()
    country_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cex_inbox'
