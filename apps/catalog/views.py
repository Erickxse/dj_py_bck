from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.stand.models import CexStand
from apps.service_product.models import CexCountry
from .models import CexCatalog
from .serializers import CexCatalogSerializer, CexCatalogDetailSerializer
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def get_catalogs_by_stand_and_country(request, country_code, stand_slug):
    try:
        # Obtener el país usando el código ISO
        country = get_object_or_404(CexCountry, iso=country_code.upper())  # Asegúrate de que el código ISO esté en mayúsculas
        
        # Obtener el stand usando el slug y el country_id
        stand = get_object_or_404(CexStand, slug=stand_slug, country=country)
        
        # Filtrar los catálogos usando stand_id y country_id
        catalogs = CexCatalog.objects.filter(stand_id=stand.id, country_id=country.id)

        if not catalogs:
            return Response({"error": "No catalogs found for this stand and country."}, status=status.HTTP_404_NOT_FOUND)

        # Serializar los catálogos
        serializer = CexCatalogSerializer(catalogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except CexCountry.DoesNotExist:
        return Response({"error": "Country not found"}, status=status.HTTP_404_NOT_FOUND)
    except CexStand.DoesNotExist:
        return Response({"error": "Stand not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_catalog_detail(request, country_code, stand_slug, catalog_slug):
    try:
        # Obtener el país usando el código ISO
        country = get_object_or_404(CexCountry, iso=country_code.upper())  # Asegúrate de que el código ISO esté en mayúsculas
        
        # Obtener el stand usando el slug y el country_id
        stand = get_object_or_404(CexStand, slug=stand_slug, country=country)
        
        # Obtener el catálogo usando el catalog_slug y el stand_id
        catalog = get_object_or_404(CexCatalog, slug=catalog_slug, stand_id=stand.id, country_id=country.id)

        # Serializar el catálogo
        serializer = CexCatalogDetailSerializer(catalog)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except CexCountry.DoesNotExist:
        return Response({"error": "Country not found"}, status=status.HTTP_404_NOT_FOUND)
    except CexStand.DoesNotExist:
        return Response({"error": "Stand not found"}, status=status.HTTP_404_NOT_FOUND)
    except CexCatalog.DoesNotExist:
        return Response({"error": "Catalog not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)