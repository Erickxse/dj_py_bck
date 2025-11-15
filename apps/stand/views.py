from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import CexPlan, CexStand, CexSubscription, CexCountry
from apps.service_product.models import CexServiceProduct
from apps.service_product.models import CexQuotes
from .serializers import CexStandSerializer, MostQuotedStandSerializer, CexStandListSerializer, PlanSerializer
from django.db.models import Subquery, OuterRef, Count
from rest_framework.permissions import AllowAny
import time


@api_view(['GET'])
@permission_classes([AllowAny])
def get_stand_info_by_id(request, id):
    # Realiza la consulta a la base de datos usando el id
    stand = get_object_or_404(CexStand, id=id)

    # Usa el serializer para convertir el objeto a JSON
    serializer = CexStandListSerializer(stand)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_stand_info(request, slug):
    # Realiza la consulta a la base de datos
    stand = get_object_or_404(CexStand, slug=slug)

    # Usa el serializer para convertir el objeto a JSON
    serializer = CexStandSerializer(stand)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_most_quoted_stands(request):
    try:
        # Obtener los 10 stands más cotizados
        most_quoted = (
            CexQuotes.objects
            .values('stand_id')
            .annotate(quotes_count=Count('stand_id'))
            .order_by('-quotes_count')[:10]
        )

        if not most_quoted:
            return Response([])

        stand_ids = [quote['stand_id'] for quote in most_quoted]
        quotes_dict = {item['stand_id']: item['quotes_count']
                       for item in most_quoted}

        # Obtener los stands y mantener el orden original
        stands = list(CexStand.objects.filter(
            id__in=stand_ids, isactive=True, isdeleted=False))
        stands.sort(key=lambda s: stand_ids.index(s.id))

        # Serializar los stands
        serializer = CexStandListSerializer(stands, many=True)

        # Agregar el campo quotes_count a cada stand serializado
        data = serializer.data
        for stand in data:
            stand['quotes_count'] = quotes_dict.get(stand['id'], 0)

        return Response(data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_stands(request, country_code):
    try:
        # Obtener el parámetro `limit` de la URL, o usar 10 como valor predeterminado
        limit = int(request.GET.get('limit', 10))
        
        # Obtener el país según el `country_code`
        country = get_object_or_404(CexCountry, iso=country_code)
        # Filtrar stands con country_code (equivale a country=country.id) isactive=True e isdeleted=False y aplicar el límite
        stands = CexStand.objects.filter(country=country.id,isactive=True, isdeleted=False)[:limit]
        # Usar el serializer para convertir los objetos a JSON
        serializer = CexStandListSerializer(stands, many=True)
        
        return Response(serializer.data)
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_active_stands(request):
        
    try:
        # Filtrar las suscripciones activas (1 = true en MariaDB)
        active_subscriptions = CexSubscription.objects.filter(active=1)
        
        # Obtener los IDs de los stands relacionados
        active_stand_ids = active_subscriptions.values_list('stand_id', flat=True)
        
        # Filtrar los stands que tengan suscripciones activas
        active_stands = CexStand.objects.filter(id__in=active_stand_ids)
        stands = CexStand.objects.filter(isactive=True, isdeleted=False)
        # Serializar los datos
        serializer = CexStandListSerializer(active_stands, many=True)
        
        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_stands(request):
    try:
        import time  # Asegúrate de importar time si no está
        start_time = time.time()

        # Obtener parámetros opcionales
        letter = request.GET.get('letter', '').strip()
        country_code = request.GET.get('country', '').strip().upper()
        plan = request.GET.get('plan', '').strip()

        queryset = CexStand.objects.filter(isactive=True, isdeleted=False)

        if letter:
            queryset = queryset.filter(stand_name__istartswith=letter)

        if country_code and country_code != "ALL":
            try:
                country = CexCountry.objects.get(iso=country_code)
                queryset = queryset.filter(country_id=country.id)
            except CexCountry.DoesNotExist:
                return Response({'error': f'País con código {country_code} no encontrado.'}, status=404)

        # Filtrar por el plan_id en la tabla CexSubscription
        if plan:
            try:
                queryset = queryset.filter(
                    id__in=CexSubscription.objects.filter(
                        plan_id=plan, active=1).values_list('stand_id', flat=True)
                )
            except ValueError:
                return Response({'error': 'El parámetro "plan" debe ser un número entero.'}, status=400)

        active_stands = queryset.order_by('stand_name')
        serializer = CexStandListSerializer(active_stands, many=True)

        end_time = time.time()
        print(f"T ARTISTAS: {end_time - start_time} segundos")
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_plans_stands(request):
    try:
        #devolver todos los planes
        plans = CexPlan.objects.all()
        
        # Serializar los datos
        serializer = PlanSerializer(plans, many=True)
        
        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)
