from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.dashboard.views.Group import IsAdminGroup
from apps.service_product.models import CexServiceProduct
from apps.stand.models import CexStand
from apps.dashboard.serializers import (
    CexServiceProductGetSerializer,
    CexServiceProductPostSerializer,
)
from apps.authentication.models import User
from django.utils.text import slugify
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from apps.category.models import CexCategory
from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Coalesce

class CexServiceProductByUserView(APIView):
    """Obtiene los productos del stand asociado al usuario autenticado sin paginación."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminGroup]

    def get(self, request):
        # Obtener el usuario autenticado
        auth_user = request.user
        
        # Buscar en la tabla `User` el usuario correspondiente
        try:
            user = User.objects.get(username=auth_user.username)  
        except User.DoesNotExist: 
            return Response({"error": "Usuario no encontrado en la base de datos"}, status=404)

        # Obtener el stand_id del usuario
        if not user.stand_id:
            return Response({"error": "El usuario no tiene un stand asignado"}, status=400)
        
        stand_id = user.stand_id

        # Filtrar productos por stand_id
        products = CexServiceProduct.objects.filter(stand_id=stand_id)
        if not products.exists():
            return Response({"error": "No hay productos para este stand"}, status=404)

        # Serializar los productos
        serializer = CexServiceProductGetSerializer(products, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request):
        """Crea un nuevo producto para el stand asociado al usuario autenticado."""
        # Obtener el usuario autenticado
        auth_user = request.user
        
        # Buscar en la tabla `User` el usuario correspondiente
        try:
            user = User.objects.get(username=auth_user.username)  
        except User.DoesNotExist: 
            return Response({"error": "Usuario no encontrado en la base de datos"}, status=404)

        # Obtener el stand_id del usuario
        if not user.stand_id:
            return Response({"error": "El usuario no tiene un stand asignado"}, status=400)
        
        stand_id = user.stand_id
        
        # Obtener el country_id basado en el stand_id
        try:
            stand = CexStand.objects.get(id=stand_id)  # Se asume que Stand tiene un campo country_id
            country_id = stand.country_id
        except CexStand.DoesNotExist:
            return Response({"error": "El stand no existe o no tiene un país asignado"}, status=404)

        # Preparar los datos del producto
        data = request.data.copy()  # Hacer una copia de los datos para modificarlos
        data['stand_id'] = stand_id  # Asignar el stand_id obtenido del usuario
        data['country_id'] = country_id  # Asignar el country_id obtenido del stand

        # Asignar valores por defecto a los campos requeridos
        data['specifications'] = "Especificación por agregar"
        data['type'] = request.data.get('tipoObra', 'product')
        data['upc'] = "2022"
        data['vr_tour'] = ""
        data['bnb_code'] = ""

        # Validar que 'name' esté presente
        if not data.get('name'):
            return Response({"error": "El campo 'name' es obligatorio para generar el slug"}, status=400)

        # Generar el slug y verificar unicidad dentro del stand
        slug = slugify(data['name']).replace('-', '_')
        data['slug'] = slug
        
        # Verificar si ya existe un producto con el mismo slug y stand_id
        if CexServiceProduct.objects.filter(stand_id=stand_id, slug=slug).exists():
            return Response({"error": "Ya existe un producto con el mismo nombre en este stand"}, status=400)

        # Asignar la fecha de creación actual si no se proporciona
        if not data.get('creation_date'):
            data['creation_date'] = timezone.now()

        # Asegurarse de que seo_id sea opcional (puede ser NULL)
        if 'seo_id' not in data:
            data['seo_id'] = None

        # Serializar y validar los datos
        serializer = CexServiceProductPostSerializer(data=data)
        if serializer.is_valid():
            product = serializer.save()
            response_serializer = CexServiceProductGetSerializer(product)
            return Response(response_serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    
class CexServiceProductByStandPaginationView(APIView):
    """Obtiene los productos del stand asociado al usuario autenticado con paginación."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminGroup]

    class ProductPagination(PageNumberPagination):
        page_size = 5  # Tamaño de página por defecto
        page_size_query_param = 'page_size'  # Parámetro para personalizar el tamaño
        max_page_size = 100  # Límite máximo de elementos por página

    def get(self, request):
        # Obtener el usuario autenticado
        auth_user = request.user
        
        # Buscar en la tabla `User` el usuario correspondiente
        try:
            user = User.objects.get(username=auth_user.username)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado en la base de datos"}, status=404)

        # Verificar si el usuario tiene un stand_id asignado
        if not user.stand_id:
            return Response({"error": "El usuario no tiene un stand asignado"}, status=400)

        # Obtener el stand_id del usuario autenticado
        stand_id = user.stand_id
        
        # Subconsulta para obtener el nombre de la categoría (name_cat_3)
        category_name_subquery = CexCategory.objects.filter(
            id=OuterRef('category_id')
        ).values('name')[:1]
        
        # Filtrar productos por stand_id y anotar el nombre de la categoría
        products = CexServiceProduct.objects.filter(stand_id=stand_id).annotate(
            name_cat_3=Coalesce(Subquery(category_name_subquery), Value(None))
        )

        # Aplicar filtros opcionales
        search = request.query_params.get('search', None)
        active = request.query_params.get('active', None)
        sort_by = request.query_params.get('sort_by', None)
        sort_order = request.query_params.get('sort_order', 'desc')
        
        # Filtrar por nombre y estado
        if search:
            products = products.filter(name__icontains=search)
        if active is not None:
            products = products.filter(active=active.lower() == 'true')
            
        # Aplicar ordenamiento
        if sort_by:
            field_mapping = {
                "name": "name",  
                "name_cat_3": "name_cat_3",  
                "counter": "counter",  
            }
            sort_field = field_mapping.get(sort_by, "creation_date") 
            order_prefix = "-" if sort_order == "desc" else ""
            products = products.order_by(f"{order_prefix}{sort_field}")
        else:
            products = products.order_by('-creation_date')
        
        if not products.exists():
            return Response({"error": "No hay productos para este stand"}, status=404)
        
        # Aplicar paginación
        paginator = self.ProductPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        
        # Serializar los productos paginados
        serializer = CexServiceProductGetSerializer(paginated_products, many=True)
        total_count = products.count()

        # Devolver respuesta con datos paginados y conteo total
        response_data = {
            "total_count": total_count,
            "products": serializer.data
        }
        return Response(response_data, status=200)
    
class CexServiceProductCountByStandView(APIView):
    """Obtiene el conteo total de productos del stand asociado al usuario autenticado."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminGroup]

    def get(self, request):
        # Obtener el usuario autenticado
        auth_user = request.user
        
        # Buscar en la tabla `User` el usuario correspondiente
        try:
            user = User.objects.get(username=auth_user.username)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado en la base de datos"}, status=404)

        # Verificar si el usuario tiene un stand_id asignado
        if not user.stand_id:
            return Response({"error": "El usuario no tiene un stand asignado"}, status=400)

        # Obtener el stand_id del usuario autenticado
        stand_id = user.stand_id

        # Contar productos por stand_id
        total_count = CexServiceProduct.objects.filter(stand_id=stand_id).count()
        
        # Devolver solo el conteo
        response_data = {
            "total_count": total_count
        }
        return Response(response_data, status=200)
    
    
class CexServiceProductByIdView(APIView):
    """Obtiene los detalles de un producto específico por su ID, verificando que pertenezca al stand del usuario autenticado."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        # Obtener el usuario autenticado
        auth_user = request.user
        
        # Buscar en la tabla `User` el usuario correspondiente
        try:
            user = User.objects.get(username=auth_user.username)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado en la base de datos"}, status=404)

        # Verificar que el usuario tenga un stand asignado
        if not user.stand_id:
            return Response({"error": "El usuario no tiene un stand asignado"}, status=400)
        
        stand_id = user.stand_id

        # Obtener el producto por ID y verificar que pertenezca al stand del usuario
        try:
            product = CexServiceProduct.objects.get(id=product_id, stand_id=stand_id)
        except CexServiceProduct.DoesNotExist:
            return Response({"error": "Producto no encontrado o no pertenece a tu stand"}, status=404)

        # Serializar el producto
        serializer = CexServiceProductGetSerializer(product)
        return Response(serializer.data, status=200)
    
    def put(self, request, product_id):
        """Actualiza un producto específico por su ID, verificando que pertenezca al stand del usuario autenticado."""
        # Obtener el usuario autenticado
        auth_user = request.user
        
        # Buscar en la tabla `User` el usuario correspondiente
        try:
            user = User.objects.get(username=auth_user.username)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado en la base de datos"}, status=404)

        # Verificar que el usuario tenga un stand asignado
        if not user.stand_id:
            return Response({"error": "El usuario no tiene un stand asignado"}, status=400)
        
        stand_id = user.stand_id

        # Obtener el producto por ID y verificar que pertenezca al stand del usuario
        try:
            product = CexServiceProduct.objects.get(id=product_id, stand_id=stand_id)
        except CexServiceProduct.DoesNotExist:
            return Response({"error": "Producto no encontrado o no pertenece a tu stand"}, status=404)

        # Preparar los datos para la actualización
        data = request.data.copy()  # Hacer una copia de los datos para modificarlos
        data['stand_id'] = stand_id  # Asegurar que el stand_id no pueda ser modificado

     # Validar que 'name' no genere un slug duplicado dentro del mismo stand
        if 'name' in data and data['name'] != product.name:
            new_slug = slugify(data['name']).replace('-', '_')
                    # Verificar si el nuevo slug ya existe en otro producto dentro del mismo stand
            if CexServiceProduct.objects.filter(stand_id=stand_id, slug=new_slug).exclude(id=product_id).exists():
                return Response({"error": "Ya existe otro producto con el mismo nombre en este stand"}, status=400)

            data['slug'] = new_slug  # Asignar el nuevo slug solo si el nombre cambió

        # Asegurarse de que seo_id sea opcional (puede ser NULL)
        if 'seo_id' not in data:
            data['seo_id'] = None

        # Serializar y validar los datos
        serializer = CexServiceProductPostSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            updated_product = serializer.save()
            response_serializer = CexServiceProductGetSerializer(updated_product)
            return Response(response_serializer.data, status=200)
        return Response(serializer.errors, status=400)
