from rest_framework import serializers
from .models import CexExhibition
from apps.stand.models import CexStand

class CexExhibitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CexExhibition
        fields = ['title','country', 'stand_id', 'date', 'slug', 'code', 'date_final']


class CexExhibitionDetailSerializer(serializers.ModelSerializer):

    stand_name = serializers.SerializerMethodField()
    stand_slug = serializers.SerializerMethodField()

    class Meta:
        model = CexExhibition
        fields = ['title', 'country', 'stand_id', 'date', 'slug', 'code', 'date_final', 'stand_name', 'stand_slug']

    def get_stand_name(self, obj):
        try:
            return CexStand.objects.get(id=obj.stand_id).stand_name
        except CexStand.DoesNotExist:
            return None
        
    def get_stand_slug(self, obj):
        try:
            return CexStand.objects.get(id=obj.stand_id).slug
        except CexStand.DoesNotExist:
            return None

