from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from apps.dashboard.models import CexQuotes
from apps.dashboard.views.Group import IsAdminGroup
from apps.service_product.models import CexServiceProduct
from apps.stand.models import CexStand
from apps.authentication.models import User
from apps.dashboard.serializers import CexQuoteSerializer, CexReportSerializer

class CexDashboardOverviewView(APIView):
    """Obtiene los últimos 10 pedidos, el reporte de cotizaciones, el nombre del stand y el totalCounter."""
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminGroup]

    def get(self, request):
        auth_user = request.user

        # 🔹 Obtener el usuario autenticado
        try:
            user = User.objects.get(username=auth_user.username)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado en la base de datos"}, status=404)

        if not user.stand_id:
            return Response({"error": "El usuario no tiene un stand asignado"}, status=400)

        stand_id = user.stand_id

        # 🔹 Obtener el nombre del stand y los hits
        stand = CexStand.objects.filter(id=stand_id).first()
        stand_name = stand.stand_name if stand else None
        image = stand.img if stand else None
        stand_hits = stand.hits if stand else 0  # Si no hay stand, los hits son 0

        # 🔹 Calcular totalCounter (suma de counter de productos + hits del stand)
        product_counter_sum = CexServiceProduct.objects.filter(stand_id=stand_id).aggregate(Sum("counter"))["counter__sum"] or 0
        total_counter = product_counter_sum + stand_hits

        # 🔹 Obtener el conteo total de productos (obras) del stand
        product_counts = CexServiceProduct.objects.filter(stand_id=stand_id).count()

        # 🔹 Obtener los últimos 10 pedidos (quotes)
        last_10_quotes = CexQuotes.objects.filter(stand_id=stand_id).order_by("-quoted_on")[:10]
        quotes_data = CexQuoteSerializer(last_10_quotes, many=True).data  

        # 🔹 Contar todas las cotizaciones del stand (Total Pedidos)
        total_orders = CexQuotes.objects.filter(stand_id=stand_id).count()

        # 🔹 Obtener **todas** las cotizaciones del stand para el reporte
        all_quotes = CexQuotes.objects.filter(stand_id=stand_id)
        report_data = CexReportSerializer(instance=all_quotes).data  

        # 🔹 Construir respuesta final
        response_data = {
            "stand_id": stand_id,
            "stand_name": stand_name,  
            "image": image,
            "totalCounter": total_counter,
            "product_counts": product_counts,
            "quotes": quotes_data,  
            "report": report_data,
            "total_orders": total_orders,
        }

        return Response(response_data, status=200)
