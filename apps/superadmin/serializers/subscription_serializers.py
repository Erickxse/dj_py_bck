from datetime import datetime, timedelta
from rest_framework import serializers
from apps.superadmin.models import CexSubscription, CexPlan


class CexSubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.SerializerMethodField()
    expiration_date = serializers.SerializerMethodField()

    def get_plan_name(self, obj):
        plan = CexPlan.objects.filter(id=obj.plan_id).first()
        if plan:
            return plan.name
        return None

    def get_expiration_date(self, obj):
        # Convertir creation_date (que es str) a datetime
        # Ajusta el formato según cómo esté guardada la cadena en la base de datos
        creation_date_str = obj.creation_date
        
        # si la fecha tiene el "/" en vez de "-" se cambia
        if "/" in creation_date_str:
            creation_date_str = creation_date_str.replace("/", "-")
        
        # Cambia el formato si es necesario
        creation_date = datetime.strptime(
            creation_date_str, '%Y-%m-%d')

        # Calcular la fecha de expiración
        expiration_date = creation_date + timedelta(days=obj.plan_valid_for)

        # Devolver la fecha en formato "Año-mes-día"
        return expiration_date.strftime('%Y-%m-%d')

    class Meta:
        model = CexSubscription
        fields = ['plan_name', 'creation_date',
                  'plan_valid_for', 'active', 'expiration_date']
