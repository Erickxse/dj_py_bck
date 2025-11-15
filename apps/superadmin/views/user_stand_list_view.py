from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from apps.superadmin.models import CexStand
from apps.authentication.models import Profile, AuthGroup, User
from apps.superadmin.views.group import IsSuperAdminGroup
from apps.superadmin.serializers.user_stand_serializer import UserStandInfoSerializer

class UserStandListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdminGroup]

    class StandPagination(PageNumberPagination):
        page_size = 5
        page_size_query_param = 'page_size'
        max_page_size = 100

    def get(self, request):
        # Obtener parámetros de consulta
        role_filter = request.query_params.get('role', None)
        sort_by = request.query_params.get('sort_by', None)
        sort_order = request.query_params.get('sort_order', 'asc')
        search_name = request.query_params.get('search_name', None)
        
        # Validar sort_by
        valid_fields = ['user_id', 'user_name', 'stand_name', 'role', 'email']
        if sort_by not in valid_fields:
            sort_by = None  # Ignore invalid sort_by values

        # Validar sort_order
        if sort_order not in ['asc', 'desc']:
            sort_order = 'asc'

        # Obtener todos los stands
        stands = CexStand.objects.all()

        # Obtener user_ids únicos
        user_ids = list(
            stands.values_list('user_id', flat=True)
            .exclude(user_id=None)
            .distinct()
        )

        # Bulk fetch de datos relacionados
        users = User.objects.filter(id__in=user_ids).values('id', 'email', 'role')
        profiles = Profile.objects.filter(user_id__in=user_ids).values('user_id', 'name')
        roles = AuthGroup.objects.all().values('id', 'name')

        # Construir mapas
        user_map = {u['id']: u for u in users}
        profile_map = {p['user_id']: p['name'] for p in profiles}
        role_map = {r['id']: r['name'] for r in roles}

        # Construir lista
        data = []
        for stand in stands:
            user_id = stand.user_id

            if user_id is None:
                user_email = None
                user_role = None
                user_name = None
            else:
                user_data = user_map.get(user_id)
                if user_data:
                    user_email = user_data.get('email')
                    user_role = role_map.get(user_data.get('role'))
                else:
                    user_email = None
                    user_role = None

                user_name = profile_map.get(user_id)

            # Aplicar filtro por rol
            if role_filter is not None:
                if role_filter.lower() == 'null' and user_role is not None:
                    continue
                elif role_filter != 'null' and user_role != role_filter:
                    continue

            data.append({
                "user_id": user_id,
                "user_name": user_name,
                "stand_name": stand.stand_name,
                "role": user_role,
                "email": user_email
            })
            # Aplicar filtro por nombre
            if search_name:
                search_name_lower = search_name.lower()
                data = [item for item in data if item['user_name'] and search_name_lower in item['user_name'].lower()]

        # Aplicar ordenamiento
        if sort_by:
            reverse = sort_order == 'desc'
            def get_sort_key(item):
                value = item.get(sort_by)
                # Handle None values by placing them at the end
                if value is None:
                    return (1,)  # Single-element tuple for None
                # Handle strings with case-insensitive sorting
                if isinstance(value, str):
                    return (0, value.lower())  # Tuple for strings
                # Handle integers (for user_id)
                return (0, value)  # Tuple for integers

            data = sorted(data, key=get_sort_key, reverse=reverse)

        # Aplicar paginación
        paginator = self.StandPagination()
        paginated_data = paginator.paginate_queryset(data, request)

        # Serializar
        serializer = UserStandInfoSerializer(paginated_data, many=True)

        # Respuesta paginada
        return Response({
            "total_count": paginator.page.paginator.count,
            "users": serializer.data
        })