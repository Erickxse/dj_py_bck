from rest_framework import serializers
from .models import CexLandingPages

class CexLandingPagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CexLandingPages
        fields = '__all__'

class CexLandingPublicPagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CexLandingPages
        fields = ['name', 'seo_description', 'slug']