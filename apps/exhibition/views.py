import time
from rest_framework import generics
from .models import CexExhibition, CexCountry
from .serializers import CexExhibitionSerializer, CexExhibitionDetailSerializer
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes([AllowAny])
def list_exhibitions_by_country(request, country_code):
    try:
        # Obtener el parámetro `limit` de la URL, o usar 10 como valor predeterminado
        limit = int(request.GET.get('limit', 10))
        
        # Obtener el país según el `country_code`
        country = get_object_or_404(CexCountry, iso=country_code)
        # Filtrar exhibiciones con country_code (equivale a country=country)  
        exhibitions = CexExhibition.objects.filter(country=country)[:limit]
        # Usar el serializer para convertir los objetos a JSON
        serializer = CexExhibitionSerializer(exhibitions, many=True)
        
        return Response(serializer.data)
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def exhibition_detail_by_country(request, country_code, slug):
    try:
        # Obtener el país según el `country_code`
        country = get_object_or_404(CexCountry, iso=country_code)
        
        # Buscar la exhibición que coincida con el slug y el país
        exhibition = get_object_or_404(CexExhibition, country=country.id, slug=slug)
        
        # Serializar la exhibición encontrada
        serializer = CexExhibitionDetailSerializer(exhibition)
        
        return Response(serializer.data)
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def exhibitions_details(request, country_code):
    # Calcular cuanto tiempo toma esta funcion
    start_time = time.time()
    try:
        limit = int(request.GET.get('limit', 10))
        country = get_object_or_404(CexCountry, iso=country_code.lower())

        exhibitions = CexExhibition.objects.filter(country_id=country.id)[:limit]
        serializer = CexExhibitionDetailSerializer(exhibitions, many=True)
        end_time = time.time()
        print(f"T EXHIBICIONES VIRTUALES: {end_time - start_time} segundos")
        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)