from rest_framework import serializers
from apps.superadmin.models import CexPlan


class CexPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CexPlan
        fields = ['id', 'name']
