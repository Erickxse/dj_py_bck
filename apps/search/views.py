from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from apps.category.models import CexCategory
from apps.stand.models import CexStand, CexCountry
from apps.service_product.models import CexServiceProduct
from .serializers import CexServiceProductSerializer, CexCategorySerializer
from apps.stand.serializers import CexStandListSerializer
from rest_framework.permissions import AllowAny


class SearchResultsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('query', '')

        # Obtener todos los productos que coincidan con la búsqueda y estén activos
        service_products = CexServiceProduct.objects.filter(name__icontains=query, active=True)
        service_products_serializer = CexServiceProductSerializer(service_products, many=True)

   # Obtener todos los stands que coincidan con la búsqueda, estén activos y no eliminados
        stands = CexStand.objects.filter(stand_name__icontains=query, isactive=True, isdeleted=False)
        stands_serializer = CexStandListSerializer(stands, many=True)

        # Obtener todas las categorías que coincidan con la búsqueda
        categories = CexCategory.objects.filter(name__icontains=query)

        categories_serializer = CexCategorySerializer(categories, many=True)

        return Response({
            'service_products': service_products_serializer.data,
            'stands': stands_serializer.data,
            'categories': categories_serializer.data,
        }, status=status.HTTP_200_OK)

        
        
class SearchPaginationView(APIView):
    permission_classes = [AllowAny]

    class ProductPagination(PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'
        max_page_size = 100

    def get(self, request):
        query = request.query_params.get('query', '').strip()
        country_param = request.query_params.get('country', '').strip().lower()

        # Filtro base
        service_products = CexServiceProduct.objects.all()
        stands = CexStand.objects.filter(isactive=True, isdeleted=False)
        categories = CexCategory.objects.filter(level=3)

        # Si hay query, filtrar por texto
        if query:
            service_products = service_products.filter(name__icontains=query)
            stands = stands.filter(stand_name__icontains=query)
            categories = categories.filter(name__icontains=query)

        # Si hay country, filtrar por país
        if country_param and country_param != 'all':
            country_obj = CexCountry.objects.filter(name__iexact=country_param).first()
            if not country_obj:
                country_obj = CexCountry.objects.filter(iso__iexact=country_param).first()

            if country_obj:
                country_id = country_obj.id
                service_products = service_products.filter(country_id=country_id)
                stands = stands.filter(country_id=country_id)
                categories = categories.filter(
                    id__in=service_products.values_list('category_id', flat=True).distinct()
                )
            else:
                return Response({
                    "error": f"No se encontró país con código o nombre '{country_param}'"
                }, status=status.HTTP_404_NOT_FOUND)

        # Paginación
        paginator = self.ProductPagination()
        paginated_products = paginator.paginate_queryset(service_products, request)
        products_serializer = CexServiceProductSerializer(paginated_products, many=True)

        # Serialización de stands y categorías
        stands_serializer = CexStandListSerializer(stands, many=True)
        categories_serializer = CexCategorySerializer(categories, many=True)

        return Response({
            'service_products': products_serializer.data,
            'total_service_products': paginator.page.paginator.count,
            'stands': stands_serializer.data,
            'total_stands': stands.count(),
            'categories': categories_serializer.data,
            'total_categories': categories.count()
        }, status=status.HTTP_200_OK)
        