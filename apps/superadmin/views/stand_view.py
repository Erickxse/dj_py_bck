from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from apps.superadmin.models import CexStand, CexSubscription, CexPlan
from apps.authentication.models import Profile
from apps.dashboard.models import CexQuotes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.superadmin.serializers.stand_serializers import CexStandSerializer
from apps.superadmin.views.group import IsSuperAdminGroup
from django.db.models import OuterRef, Subquery, Value,Count
from django.db.models.functions import Coalesce
from rest_framework import status

class AllStandsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdminGroup]
    
    class StandPagination(PageNumberPagination):
        page_size = 5  # Tamaño de página por defecto
        page_size_query_param = 'page_size'  # Parámetro para personalizar el tamaño
        max_page_size = 100  # Límite máximo de elementos por página

    def get(self, request):
        # Obtener todos los stands
        stands = CexStand.objects.all()

        # Aplicar filtros opcionales
        search_id = request.query_params.get('search_id', None)  # Filtro por stand_id
        search_name = request.query_params.get('search_name', None)  # Filtro por stand_name
        active_status = request.query_params.get('active_status', None)  # Filtro por estado (0 o 1)
        sort_by = request.query_params.get('sort_by', None)  # Campo para ordenar
        sort_order = request.query_params.get('sort_order', 'desc')  # Orden por defecto descendente

        # Filtrar por stand_id si se proporciona
        if search_id:
            stands = stands.filter(id__contains=search_id)

        # Filtrar por stand_name si se proporciona
        if search_name:
            stands = stands.filter(stand_name__icontains=search_name)

        # Subconsulta para obtener el active_status más reciente desde CexSubscription
        active_status_subquery = CexSubscription.objects.filter(
            stand_id=OuterRef('id')
        ).order_by('-creation_date').values('active')[:1]

        # Subconsulta para obtener el plan_name desde CexSubscription y CexPlan
        plan_id_subquery = CexSubscription.objects.filter(
            stand_id=OuterRef('id')
        ).order_by('-creation_date').values('plan_id')[:1]
        
        plan_name_subquery = CexPlan.objects.filter(
            id=Subquery(plan_id_subquery)
        ).values('name')[:1]

        # Subconsulta para obtener expiration_date (necesitamos creation_date y plan_valid_for)
        creation_date_subquery = CexSubscription.objects.filter(
            stand_id=OuterRef('id')
        ).order_by('-creation_date').values('creation_date')[:1]

        plan_valid_for_subquery = CexSubscription.objects.filter(
            stand_id=OuterRef('id')
        ).order_by('-creation_date').values('plan_valid_for')[:1]

        # Subconsulta para total_pedidos desde CexQuotes
        total_pedidos_subquery = CexQuotes.objects.filter(
            stand_id=OuterRef('id')
        ).values('stand_id').annotate(total=Count('id')).values('total')[:1]

        # Anotar los campos necesarios para filtrado y ordenamiento
        stands = stands.annotate(
            active_status_annotation=Coalesce(Subquery(active_status_subquery), Value(None)),
            plan_name_annotation=Coalesce(Subquery(plan_name_subquery), Value(None)),
            creation_date_annotation=Coalesce(Subquery(creation_date_subquery), Value(None)),
            plan_valid_for_annotation=Coalesce(Subquery(plan_valid_for_subquery), Value(None)),
            total_pedidos_annotation=Coalesce(Subquery(total_pedidos_subquery), Value(0))
        )

        # Filtrar por active_status si se proporciona
        if active_status is not None:
            try:
                active_value = int(active_status)
                if active_value not in [0, 1]:
                    return Response({"error": "active_status debe ser 0 o 1"}, status=400)
                stands = stands.filter(active_status_annotation=active_value)
            except ValueError:
                return Response({"error": "active_status debe ser un número (0 o 1)"}, status=400)

        # Aplicar ordenamiento
        if sort_by:
            # Mapear los campos para ordenamiento
            field_mapping = {
                "id": "id",
                "stand_name": "stand_name",
                "slug": "slug",
                "hits": "hits",
                "plan_name": "plan_name_annotation",
                "expiration_date": "creation_date_annotation",  # Usamos creation_date como proxy
                "total_pedidos": "total_pedidos_annotation",
            }
            sort_field = field_mapping.get(sort_by, "id")  # Por defecto id si el campo no es válido
            order_prefix = "-" if sort_order == "desc" else ""
            stands = stands.order_by(f"{order_prefix}{sort_field}")
        else:
            stands = stands.order_by('-id')  # Orden por defecto descendente por id

        if not stands.exists():
            return Response({"error": "No stands found with the given filters"}, status=404)

        # Aplicar paginación
        paginator = self.StandPagination()
        paginated_stands = paginator.paginate_queryset(stands, request)

        # Serializar los stands paginados
        serializer = CexStandSerializer(paginated_stands, many=True)
        total_count = stands.count()

        # Estructurar la respuesta
        response_data = {
            "total_count": total_count,
            "stands": serializer.data
        }

        return Response(response_data, status=200)

class StandDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdminGroup]

    def get(self, request, id):
        try:
            stand = CexStand.objects.get(id=id)
            serializer = CexStandSerializer(stand)
            data = serializer.data

            # Extraer el perfil asociado al stand
            try:
                profile = Profile.objects.get(user_id=stand.user_id)
                profile_data = {
                    "public_email": profile.public_email,
                    "first_name": profile.cex_first_name,
                    "last_name": profile.cex_last_name,
                    "cex_contact_phone": profile.cex_contact_phone,
                    "cex_city": profile.cex_city,
                    "country": profile.cex_country_id,
                    "province": profile.cex_province_id,
                }
                data["profile"] = profile_data
            except Profile.DoesNotExist:
                data["profile"] = None

            # Extraer el campo tour_virtual_active y convertirlo correctamente
            raw_active = getattr(stand, 'tour_virtual_active', 0)
            if isinstance(raw_active, (bytes, bytearray)):
                tour_virtual_active = int.from_bytes(raw_active, 'big')
            else:
                try:
                    tour_virtual_active = int(raw_active)
                except Exception:
                    tour_virtual_active = 0
            data['tour_virtual_active'] = tour_virtual_active

           # Incluir tour_virtual_code siempre, independientemente de tour_virtual_active
            data['tour_virtual_code'] = getattr(stand, 'tour_virtual_code', None)

            return Response(data, status=status.HTTP_200_OK)
        except CexStand.DoesNotExist:
            return Response({"error": "Stand not found"}, status=status.HTTP_404_NOT_FOUND)