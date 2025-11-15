from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.superadmin.views.group import IsSuperAdminGroup

from apps.superadmin.models import CexSubscription, CexPlan
from apps.superadmin.serializers.subscription_serializers import CexSubscriptionSerializer
from apps.authentication.models import User
from django.utils import timezone
from django.db import transaction, IntegrityError


class SubscriptionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdminGroup]

    def get(self, request, stand_id):
        # Obtener todas las suscripciones para el stand_id
        subscriptions = CexSubscription.objects.filter(stand_id=stand_id).order_by('id')

        if subscriptions.exists():  # Verifica si hay al menos una suscripción
            serialized_data = CexSubscriptionSerializer(
                subscriptions, many=True).data 
            return Response(serialized_data, status=200)
        else:
            return Response({"error": "No se encontró la suscripción activa"}, status=404)
    
    def post(self, request, stand_id):
        print(request.data)
        plan_name = request.data.get('plan_name')
        plan_valid_for = request.data.get('plan_valid_for')
        note = request.data.get('note')
        
        plan_valid_for = int(plan_valid_for) if plan_valid_for else 0
        
        # Verificar si el stand_id y el plan_id son válidos
        if not stand_id or not plan_name:
            return Response({"error": "stand_id y plan_id son requeridos"}, status=400)
        
        plan = get_object_or_404(CexPlan, id=plan_name)
        user = get_object_or_404(User, stand_id=stand_id)
        
        try:
            with transaction.atomic():
                # Desactivar la suscripción anterior si existe
                previous_subscription = CexSubscription.objects.filter(
                    stand_id=stand_id, active=True).last()
                if previous_subscription:
                    previous_subscription.active = False
                    previous_subscription.save()

                # Crear una nueva suscripción
                newSubscription = CexSubscription.objects.create(
                    creation_date=timezone.now().strftime('%Y-%m-%d'),  # Formato "Año-mes-día"
                    active=True,
                    stand_id=stand_id,
                    plan_id=plan.id,
                    plan_valid_for=plan_valid_for,
                    note = note,
                    edit_user = user.id,
                    months = plan_valid_for / 31
                )
                newSubscription.save()
                return Response({"message": "Suscripción creada exitosamente"}, status=201)
            
        except IntegrityError:
            #Revertir los cambios
            transaction.rollback()

            if 'newSubscription' in locals():
                newSubscription.delete()

            previous_subscription.active = True
            previous_subscription.save()
            
            # Manejar el error de integridad
            return Response({"error": "Error de integridad en la base de datos"}, status=500)
            
        except Exception as e:
            if 'newSubscription' in locals():
                newSubscription.delete()

            previous_subscription.active = True
            previous_subscription.save()
            return Response({"error": str(e)}, status=500)
        
        
        
        

