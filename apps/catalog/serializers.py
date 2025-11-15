from rest_framework import serializers
from .models import CexCatalog
from apps.stand.models import CexStand
from apps.service_product.models import CexCountry

class CexCatalogSerializer(serializers.ModelSerializer):
    stand_slug = serializers.SerializerMethodField()
    country_iso = serializers.SerializerMethodField()

    class Meta:
        model = CexCatalog
        fields = ['id', 'title', 'description', 'slug', 'img_pdf', 'stand_slug', 'country_iso', 'url']

    def get_stand_slug(self, obj):
        # Obtén el slug del stand asociado al catálogo
        try:
            stand = CexStand.objects.get(id=obj.stand_id)
            return stand.slug if stand else None
        except CexStand.DoesNotExist:
            return None

    def get_country_iso(self, obj):
        # Obtén el código ISO del país relacionado con el catálogo
        try:
            country = CexCountry.objects.get(id=obj.country_id)
            return country.iso.lower()  # Devuelve el ISO en minúsculas
        except CexCountry.DoesNotExist:
            return None

class CexCatalogDetailSerializer(serializers.ModelSerializer):

    stand_img= serializers.SerializerMethodField()

    class Meta:
        model = CexCatalog
        fields = ['stand_id', 'title', 'description', 'img_pdf', 'url', 'slug', 'stand_img']

    def get_stand_img(self, obj):
        # Obtén la imagen del stand asociada al catálogo
        try:
            stand = CexStand.objects.get(id=obj.stand_id)
            return stand.img if stand else None
        except CexStand.DoesNotExist:
            return None