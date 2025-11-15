from rest_framework import serializers
from apps.superadmin.models import CexStand, CexSubscription, CexPlan
from apps.dashboard.models import CexQuotes
from django.utils import timezone

class CexStandSerializer(serializers.ModelSerializer):
    plan_name = serializers.SerializerMethodField()
    expiration_date = serializers.SerializerMethodField()
    active_status = serializers.SerializerMethodField()
    total_pedidos = serializers.SerializerMethodField()
    
    class Meta:
        model = CexStand
        fields = ['id', 'stand_name', 'slug', 'hits', 'plan_name', 'expiration_date','active_status','total_pedidos']

    def get_plan_name(self, obj):
        try:
            # Obtener la suscripción más reciente, sin filtrar por active
            subscription = CexSubscription.objects.filter(
                stand_id=obj.id
            ).order_by('-creation_date').first()  # Ordenar por fecha descendente
            
            if subscription:
                plan = CexPlan.objects.get(id=subscription.plan_id)
                return plan.name
            return None
        except (CexSubscription.DoesNotExist, CexPlan.DoesNotExist):
            return None

    def get_expiration_date(self, obj):
        try:
            # Obtener la suscripción más reciente, sin filtrar por active
            subscription = CexSubscription.objects.filter(
                stand_id=obj.id
            ).order_by('-creation_date').first()  # Más reciente primero
            
            if subscription:
                # Convertir creation_date a datetime
                creation_date = timezone.datetime.strptime(
                    subscription.creation_date, 
                    '%Y/%m/%d'
                )
                # Calcular la fecha de expiración sumando los días de plan_valid_for
                expiration = creation_date + timezone.timedelta(
                    days=subscription.plan_valid_for
                )
                return expiration.strftime('%Y/%m/%d')
            return None
        except (CexSubscription.DoesNotExist, ValueError) as e:
            print(f"Error procesando expiration_date para stand {obj.id}: {str(e)}")
            return None

    def get_active_status(self, obj):
        try:
        # Obtener el estado de la suscripción más reciente
            stand = CexStand.objects.get(id=obj.id)

            # Convertir bytes a booleano y luego a string
            if isinstance(stand.isactive, bytes):
                is_active = stand.isactive == b'\x01'
            else:
                is_active = bool(stand.isactive)

            return "Sí" if is_active else "No"

        except CexStand.DoesNotExist:
            return "No"
        
    def get_total_pedidos(self, obj):
        try:
            # Contar el total de pedidos (CexQuotes) para este stand
            total = CexQuotes.objects.filter(stand_id=obj.id).count()
            return total
        except Exception as e:
            print(f"Error contando pedidos para stand {obj.id}: {str(e)}")
            return 0  # Devolver 0 si hay un error
