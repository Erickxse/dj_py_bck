import time
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Count, F, Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .models import CexServiceProduct, CexQuotes, CexCountry
from apps.stand.models import CexStand
from apps.category.models import CexCategory
from .serializers import CexCategoriesNamesDataSerializer, CexServiceProductSerializer, CexServiceProductDataSerializer
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound

#Fuction t get top products by slug stand
@api_view(['GET'])
@permission_classes([AllowAny])
def get_top_products_by_stand(request, slug, country_code):
    try:
        # Obtener el pais del URL
        country = get_object_or_404(CexCountry, iso=country_code)
        
        stand = CexStand.objects.get(slug=slug, country=country.id)
        stand_id = stand.id
        
        top_products_data = (
            CexQuotes.objects
            .filter(stand_id=stand_id)
            .exclude(service_product_id=None)  # Excluir None
            .values('service_product_id')
            .annotate(product_count=Count('service_product_id'))
            .order_by('-product_count')[:10]
        )

        product_ids_in_order = [item['service_product_id'] for item in top_products_data]

        top_products = CexServiceProduct.objects.filter(id__in=product_ids_in_order)

        products_by_id = {product.id: product for product in top_products}

        # Filtrar para evitar KeyError
        ordered_products = [products_by_id.get(product_id) for product_id in product_ids_in_order if product_id in products_by_id]

        # Serializar solo los productos que se encontraron
        serializer = CexServiceProductSerializer(ordered_products, many=True)

        return Response(serializer.data)
    except CexStand.DoesNotExist:
        return Response({"error": "Stand not found"}, status=status.HTTP_404_NOT_FOUND)

#Fuction t get recent products by slug stand
@api_view(['GET'])
@permission_classes([AllowAny])
def get_top_products(request, country_code):
    limit = request.GET.get('limit', 10)  # Obtener el parámetro limit, por defecto 10
    try:
        limit = int(limit)  # Convertir a entero
    except ValueError:
        return Response({"error": "Limit must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    # Obtener el pais del URL
    country = get_object_or_404(CexCountry, iso=country_code)

    # Obtener los productos más populares en general
    top_products_data = (
        CexQuotes.objects
        .exclude(service_product_id=None)
        .filter(service_product_id__in=CexServiceProduct.objects.filter(country=country.id).values('id')) # Filtrar por país dentro del service producto, no del cexquotes
        .values('service_product_id')
        .annotate(product_count=Count('service_product_id'))
        .order_by('-product_count')[:limit]
    )

    product_ids_in_order = [item['service_product_id'] for item in top_products_data]

    top_products = CexServiceProduct.objects.filter(id__in=product_ids_in_order)

    products_by_id = {product.id: product for product in top_products}

    # Filtrar para evitar KeyError
    ordered_products = [products_by_id.get(product_id) for product_id in product_ids_in_order if product_id in products_by_id]

    # Serializar solo los productos que se encontraron
    serializer = CexServiceProductSerializer(ordered_products, many=True)

    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([AllowAny])
def get_recent_products_by_stand(request, slug, country_code):
    
    category = request.query_params.get('category', None)
    price_min = request.query_params.get('price_min', None)
    price_max = request.query_params.get('price_max', None)
    sortBy = request.query_params.get('sort_by', None)
    
    limit = request.GET.get('limit', 10)  # Obtener el parámetro limit, por defecto 10
    try:
        limit = int(limit)  # Convertir a entero
    except ValueError:
        return Response({"error": "Limit must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Obtener el pais del URL
        country = get_object_or_404(CexCountry, iso=country_code)
        
        # Obtener el stand a partir del slug
        stand = CexStand.objects.get(slug=slug, country=country.id)
        stand_id = stand.id
        
        # Obtener los productos añadidos recientemente
        recent_products = CexServiceProduct.objects.filter(stand_id=stand_id)

        if category:
            recent_products = recent_products.filter(category_id=category)
        if price_min:
            recent_products = recent_products.filter(price__gte=price_min)
        if price_max:
            recent_products = recent_products.filter(price__lte=price_max)
        if sortBy:
            if sortBy == 'price_asc':
                recent_products = recent_products.order_by('price')
            elif sortBy == 'price_desc':
                recent_products = recent_products.order_by('-price')
            elif sortBy == 'creation_date':
                recent_products = recent_products.order_by('creation_date')
            else:
                return Response({"error": "Invalid sort parameter"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            recent_products = recent_products.order_by('-creation_date')

        recent_products = recent_products[:limit]
        # Serializar los productos
        serializer = CexServiceProductSerializer(recent_products, many=True)

        return Response(serializer.data)
    except CexStand.DoesNotExist:
        return Response({"error": "Stand not found"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def get_categories_by_stand_slug(request, slug, country_code):
    try:
        country = get_object_or_404(CexCountry, iso=country_code)
        
        # Obtener el stand a partir del slug
        stand = CexStand.objects.get(slug=slug, country=country.id)
        stand_id = stand.id

        # Obtener los productos añadidos recientemente
        recent_products = CexServiceProduct.objects.filter(stand_id=stand_id)
        
        #obtener las categorias de los productos sin repetir
        categories = recent_products.values('category_id').annotate(category_count=Count('category_id')).order_by('-category_count')
        
        # Obtener los IDs de las categorías
        category_ids = [category['category_id'] for category in categories]
        
        # Obtener las categorías a partir de los IDs
        categories = CexCategory.objects.filter(id__in=category_ids)
        
        # Serializar las categorías
        serializer = CexCategoriesNamesDataSerializer(categories, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except CexCategory.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_recent_products(request, country_code):
    #time how long it takes to execute the function
    start_time = time.time()
    limit = request.GET.get('limit', 10)  # Obtener el parámetro limit, por defecto 10
    try:
        limit = int(limit)  # Convertir a entero
    except ValueError:
        return Response({"error": "Limit must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    country = get_object_or_404(CexCountry, iso=country_code)
    print(f"Country: {country.id}")

    # Obtener los productos añadidos recientemente
    recent_products = (CexServiceProduct.objects
        .filter(country=country.id) # Filtrar por país
        .order_by('-creation_date') # Ordena por fecha de creación
        [:limit]
    )
    # Serializar los productos
    serializer = CexServiceProductDataSerializer(recent_products, many=True)
    end_time = time.time()
    print(f"T RECENT PRODUCTS: {end_time - start_time} segundos")
    return Response(serializer.data)


#Fuction t get products by slug stand

@api_view(['GET'])
@permission_classes([AllowAny])
def get_products_by_stand(request, slug, country_code):
    try:
        # Obtener el pais del URL
        country = get_object_or_404(CexCountry, iso=country_code)
        
        # Obtener el stand a partir del slug
        stand = CexStand.objects.get(slug=slug)
        stand_id = stand.id
        
        # Obtener todos los productos asociados a este stand
        products = CexServiceProduct.objects.filter(stand_id=stand_id)

        # Serializar los productos
        serializer = CexServiceProductDataSerializer(products, many=True)

        # Devolver los datos serializados
        return Response(serializer.data, status=status.HTTP_200_OK)
    except CexStand.DoesNotExist:
        return Response({"error": "Stand not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# Function to get product details by stand_slug and product_slug (obra_slug)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_by_slug(request, stand_slug, product_slug, country_code):
    try:
        # Obtener el país del URL
        country = get_object_or_404(CexCountry, iso=country_code)
        
        # Busca el stand primero para obtener su ID
        stand = CexStand.objects.filter(slug=stand_slug).first()
        if not stand:
            return Response({"error": "Stand no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        product = CexServiceProduct.objects.filter(stand_id=stand.id, slug=product_slug).first()
        if product:
            serializer = CexServiceProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Obra no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Capturar detalles adicionales
        return Response({"error": str(e), "details": repr(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_trending_products(request, country_code):
    
    #time how long it takes to execute the function
    start_time = time.time()
    limit = request.GET.get('limit', 10)  # Parámetro opcional para limitar resultados
    try:
        limit = int(limit)
    except ValueError:
        return Response({"error": "Limit must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    # Obtener el país del URL
    country = get_object_or_404(CexCountry, iso=country_code)

    # Obtener productos ordenados por counter (más vistos primero)
    trending_products = CexServiceProduct.objects.filter(country = country.id).order_by('-counter')[:limit]

    # Usar el serializer para serializar los productos
    serializer = CexServiceProductDataSerializer(trending_products, many=True)
    
    end_time = time.time()
    print(f"T TRENDING PRODUCTS: {end_time - start_time} segundos")
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_products_by_level_3_category(request, category_slug, country_code):
    try:
        # Obtener el país del URL
        country = get_object_or_404(CexCountry, iso=country_code)
        
        # Buscar la categoría de nivel 3 usando el slug proporcionado
        level_3_category = get_object_or_404(CexCategory, slug=category_slug, level=3)
        
        # Filtrar los productos que tengan esta categoría como category_id
        products = CexServiceProduct.objects.filter(category_id=level_3_category.id, country=country.id)
        
        # Serializar los productos encontrados
        serializer = CexServiceProductSerializer(products, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        # Manejar cualquier error y devolver una respuesta de error con detalles
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#OBTENER LOS PRODUCTOS PAGINADOS POR CATEGORIA DE NIVEL 3
@api_view(['GET'])
@permission_classes([AllowAny])
def get_products_pagination_by_level_3_category(request, category_slug, country_code):
    try:
        # Clase de paginación personalizada
        class ProductPagination(PageNumberPagination):
            page_size = 10  # Tamaño por página por defecto
            page_size_query_param = 'page_size'  # Parámetro opcional para personalizar el tamaño
            max_page_size = 100  # Tamaño máximo permitido

        # Obtener el país del URL
        country = get_object_or_404(CexCountry, iso=country_code)

        # Buscar la categoría de nivel 3 usando el slug proporcionado
        try:
            level_3_category = CexCategory.objects.get(slug=category_slug, level=3)
        except CexCategory.DoesNotExist:
            return Response(
                {"error": f"Category with slug '{category_slug}' not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Filtrar los productos que tengan esta categoría como category_id
        products = CexServiceProduct.objects.filter(
            category_id=level_3_category.id, 
            country=country.id
        ).order_by('-creation_date')  # Ordenamos por fecha de creación descendente

        # Aplicar la paginación a los productos
        paginator = ProductPagination()
        
        try:
            result_page = paginator.paginate_queryset(products, request)
            if not result_page:
                return Response(
                    {"error": "No hay más productos en esta categoría."}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        except NotFound:
            return Response(
                {"error": "Página no válida o fuera de rango."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CexServiceProductSerializer(result_page, many=True)

        # Construir manualmente la respuesta para ajustar el orden
        return Response({
            "products": serializer.data,  # Lista de productos
            "total_products": products.count(),  # Total de productos
        }, status=status.HTTP_200_OK)

    except CexCountry.DoesNotExist:
        return Response(
            {"error": f"Country with ISO code '{country_code}' not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        # Log the full error for debugging
        import traceback
        print(f"Error in get_products_pagination_by_level_3_category: {str(e)}")
        print(traceback.format_exc())
        
        # Manejar cualquier error y devolver una respuesta de error con detalles
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_similar_products(request, category_id, stand_slug, country_code):
    try:
        # Obtener el país
        country = get_object_or_404(CexCountry, iso=country_code)
        
        # Obtener el stand a partir del slug
        stand = CexStand.objects.get(slug=stand_slug, country=country.id)
        stand_id = stand.id
        
        # Filtrar los productos por category_id y stand_id
        products = CexServiceProduct.objects.filter(category_id=category_id, stand_id=stand_id)

        # Serializar los productos
        serializer = CexServiceProductDataSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except CexStand.DoesNotExist:
        return Response({"error": "Stand not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
