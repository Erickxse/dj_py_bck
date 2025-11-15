
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.dashboard.models import CexQuotes
from apps.dashboard.serializers.quote_serializers import CexQuoteDetailsSerializer
from apps.dashboard.views.Group import IsAdminGroup
from rest_framework.pagination import PageNumberPagination
from apps.authentication.models import User
from apps.dashboard.serializers import CexQuoteSerializer, CexQuoteByStandSerializer, CexReportSerializer
from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Coalesce
from apps.service_product.models import CexServiceProduct
from apps.category.models import CexCategory

class CexQuoteByUserView(APIView):
    """Obtiene los últimos 10 pedidos del stand asociado al usuario autenticado, ordenados por fecha descendente."""
    authentication_classes = [TokenAuthentication]
    # ← Requiere autenticación
    permission_classes = [IsAuthenticated, IsAdminGroup]

    def get(self, request):
        # Obtener el usuario autenticado
        auth_user = request.user
        
        # Buscar el usuario en la base de datos
        try:
            user = User.objects.get(username=auth_user.username)  
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado en la base de datos"}, status=404)

        # Obtener el stand_id del usuario
        if not user.stand_id:
            return Response({"error": "El usuario no tiene un stand asignado"}, status=400)
        
        stand_id = user.stand_id

        # Filtrar cotizaciones (quotes) por stand_id y ordenar por fecha descendente
        quotes = CexQuotes.objects.filter(stand_id=stand_id).order_by('-quoted_on')[:10]

        if not quotes.exists():
            return Response({"error": "No hay cotizaciones para este stand"}, status=404)

        # Serializar las cotizaciones
        serializer = CexQuoteSerializer(quotes, many=True)
        return Response(serializer.data, status=200)


class CexReportView(APIView):
    """Vista para obtener el reporte de cotizaciones agrupadas por año y mes, solo para el usuario autenticado."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Obtener el usuario autenticado
        auth_user = request.user
        
        # Buscar en la tabla `User` el usuario correspondiente
        try:
            user = User.objects.get(username=auth_user.username)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado en la base de datos"}, status=404)

        # Verificar si el usuario tiene un `stand_id` asignado
        if not user.stand_id:
            return Response({"error": "El usuario no tiene un stand asignado"}, status=400)
        
        stand_id = user.stand_id  # 🔹 Obtener el stand del usuario autenticado

        # Filtrar cotizaciones por `stand_id`
        quotes = CexQuotes.objects.filter(stand_id=stand_id)

        # Si no hay cotizaciones, devolver un error
        if not quotes.exists():
            return Response({"error": "No hay cotizaciones para este stand"}, status=404)

        # Pasar el queryset filtrado al serializador
        serializer = CexReportSerializer(instance=quotes)
        return Response(serializer.data, status=200)

class CexPaginationQuoteByStandView(APIView):
    """Obtiene todas las cotizaciones asociadas al stand del usuario autenticado, requiere autenticación."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    class QuotePagination(PageNumberPagination):
        page_size = 5  # Tamaño de página por defecto
        page_size_query_param = 'page_size'  # Parámetro para personalizar el tamaño
        max_page_size = 100  # Límite máximo de elementos por página

    def get(self, request):
        # Obtener el usuario autenticado
        auth_user = request.user
        
        # Buscar el usuario en la base de datos
        try:
            user = User.objects.get(username=auth_user.username)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado en la base de datos"}, status=404)

        # Verificar si el usuario tiene un stand_id asignado
        if not user.stand_id:
            return Response({"error": "El usuario no tiene un stand asignado"}, status=400)

        # Obtener el stand_id del usuario autenticado
        stand_id = user.stand_id

        # Realacionar CexQuotes con CexServiceProduct y CexCategory para obtener los nombres de producto y categoría
        
        # Subconsulta para obtener product_name
        product_name_subquery = CexServiceProduct.objects.filter(
            id=OuterRef('service_product_id')
        ).values('name')[:1]

        # Subconsulta para obtener category_id desde CexServiceProduct
        category_id_subquery = CexServiceProduct.objects.filter(
            id=OuterRef('service_product_id')
        ).values('category_id')[:1]

        # Anotar el category_id en la consulta de CexQuotes
        quotes = CexQuotes.objects.filter(stand_id=stand_id).annotate(
            product_name=Coalesce(Subquery(product_name_subquery), Value(None)),
            category_id=Coalesce(Subquery(category_id_subquery), Value(None))
        )
        
        # Subconsulta para obtener category_name usando el category_id anotado
        category_name_subquery = CexCategory.objects.filter(
            id=OuterRef('category_id')
        ).values('name')[:1]

        # Anotar el category_name
        quotes = quotes.annotate(
            category_name=Coalesce(Subquery(category_name_subquery), Value(None))
        )
          
        # Aplicar filtros opcionales
        search = request.query_params.get('search', None)
        status = request.query_params.get('status', None)
        sort_by = request.query_params.get('sort_by', None)
        sort_order = request.query_params.get('sort_order', 'desc')  # Por defecto descendente
        
        # Filtrar por campo quoted_by y status si se proporcionan
        if search:
            quotes = quotes.filter(quoted_by__icontains=search)
        if status:
            quotes = quotes.filter(status=status)
        
        # Aplicar ordenamiento
        if sort_by:
            # Mapear los accessorKey a los campos reales del modelo o de las tablas relacionadas
            field_mapping = {
                "quoted_by": "quoted_by",
                "product_name": "product_name",  # Campo en la tabla relacionada CexServiceProduct
                "category_name": "category_name",  # Campo en la tabla relacionada CexCategory
                "quote_phone": "quote_phone",
            }
            sort_field = field_mapping.get(sort_by, "quoted_on")  # Por defecto quoted_on si el campo no es válido
            order_prefix = "-" if sort_order == "desc" else ""
            quotes = quotes.order_by(f"{order_prefix}{sort_field}")
        else:
            quotes = quotes.order_by('-quoted_on')  # Orden por defecto
            
        
        if not quotes.exists():
            return Response({"error": "No hay cotizaciones para este stand"}, status=404)
        
        # Aplicar paginación
        paginator = self.QuotePagination()
        paginated_quotes = paginator.paginate_queryset(quotes, request)
        
        # Serializar las cotizaciones paginadas
        serializer = CexQuoteByStandSerializer(paginated_quotes, many=True)
        total_count = quotes.count()
        # Devolver un objeto que incluya los datos y el conteo
        
        response_data = {
            "total_count": total_count,
            "quotes": serializer.data
        }
        return Response(response_data, status=200)
    
class CexQuoteByStandView(APIView):
    """Obtiene todas las cotizaciones asociadas al stand del usuario autenticado, requiere autenticación."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Obtener el usuario autenticado
        auth_user = request.user
        
        # Buscar el usuario en la base de datos
        try:
            user = User.objects.get(username=auth_user.username)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado en la base de datos"}, status=404)

        # Verificar si el usuario tiene un stand_id asignado
        if not user.stand_id:
            return Response({"error": "El usuario no tiene un stand asignado"}, status=400)

        # Obtener el stand_id del usuario autenticado
        stand_id = user.stand_id

        # Filtrar cotizaciones por stand_id
        quotes = CexQuotes.objects.filter(stand_id=stand_id).order_by('-quoted_on')
        
        if not quotes.exists():
            return Response({"error": "No hay cotizaciones para este stand"}, status=404)
        
        # Serializar las cotizaciones
        serializer = CexQuoteByStandSerializer(quotes, many=True)
        total_count = quotes.count()
        # Devolver un objeto que incluya los datos y el conteo
        
        response_data = {
            "total_count": total_count,
            "quotes": serializer.data
        }
        return Response(response_data, status=200)

    
class CexQuoteCountByStandView(APIView):
    """Obtiene el conteo de cotizaciones asociadas al stand del usuario autenticado, requiere autenticación."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Obtener el usuario autenticado
        auth_user = request.user
        
        # Buscar el usuario en la base de datos
        try:
            user = User.objects.get(username=auth_user.username)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado en la base de datos"}, status=404)

        # Verificar si el usuario tiene un stand_id asignado
        if not user.stand_id:
            return Response({"error": "El usuario no tiene un stand asignado"}, status=400)

        # Obtener el stand_id del usuario autenticado
        stand_id = user.stand_id

        # Contar las cotizaciones asociadas al stand_id
        total_count = CexQuotes.objects.filter(stand_id=stand_id).count()
        
        # Si no hay cotizaciones, devolver 0 en lugar de un error
        # (puedes ajustar esto para devolver un error 404 si prefieres)
        if total_count == 0:
            return Response({"total_count": 0}, status=200)
        
        # Devolver solo el conteo
        response_data = {
            "total_count": total_count
        }
        return Response(response_data, status=200)
    
class CexQuoteDetailsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, quote_id):
        # Obtener el usuario autenticado
        auth_user = request.user

        # Buscar el usuario en la base de datos
        try:
            user = User.objects.get(username=auth_user.username)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado en la base de datos"}, status=404)

        # Verificar si el usuario tiene un stand_id asignado
        if not user.stand_id:
            return Response({"error": "El usuario no tiene un stand asignado"}, status=400)

        # Obtener el stand_id del usuario autenticado
        stand_id = user.stand_id
        
        quote = get_object_or_404(
            CexQuotes, id=quote_id, stand_id=stand_id)
        
        if not quote:
            return Response({"error": "Cotización no encontrada"}, status=404)
        
        serializer = CexQuoteDetailsSerializer(quote)  # Serializa el objeto
        return Response(serializer.data, status=200)
    
    def put(self, request, quote_id):
        quote = get_object_or_404(CexQuotes, id=quote_id)

        if quote.status == 'Nuevo':
            quote.status = 'Abierto'
        else:
            # Usa el valor actual si no se envía uno nuevo
            quote.status = request.data.get('status', quote.status)

        quote.save(update_fields=['status'])  # Solo actualiza el campo status

        return Response({"message": "Estado de la cotización actualizado"}, status=200)