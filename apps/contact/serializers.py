from rest_framework import serializers
from .models import CexInbox
from apps.authentication.models import CexCountry
from datetime import datetime

class CexInboxSerializer(serializers.ModelSerializer):
    country = serializers.CharField(write_only=True)

    class Meta:
        model = CexInbox
        fields = ['name', 'phone', 'email', 'organization', 'message', 'status', 'country']

    def create(self, validated_data):
        # Aquí tomamos directamente el nombre del país tal como viene del frontend
        country_name = validated_data.pop('country')

        try:
            country = CexCountry.objects.get(name=country_name)
        except CexCountry.DoesNotExist:
            raise serializers.ValidationError({'country': 'Nombre de país no válido.'})

        inbox = CexInbox.objects.create(
            name=validated_data.get('name'),
            phone=validated_data.get('phone'),
            email=validated_data.get('email'),
            organization=validated_data.get('organization'),
            message=validated_data.get('message'),
            status=validated_data.get('status', 'received'),
            mailed_it=datetime.now(),
            country_id=country.id
        )
        return inbox
