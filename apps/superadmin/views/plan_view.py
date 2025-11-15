from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.superadmin.views.group import IsSuperAdminGroup

from apps.superadmin.models import CexSubscription, CexPlan
from apps.superadmin.serializers.plan_serializers import CexPlanSerializer


class PlanView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdminGroup]

    def get(self, request):
        # Obtener todas los planes 
        plans = CexPlan.objects.all()

        if plans.exists():  # Verifica si hay planes
            serialized_data = CexPlanSerializer(
                plans, many=True).data
            return Response(serialized_data, status=200)
        else:
            return Response({"error": "No se encontró planes"}, status=404)
