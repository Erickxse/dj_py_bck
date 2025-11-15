from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
# from rest_framework_simplejwt.tokens import RefreshToken ->Ya no se usaría
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from rest_framework.permissions import AllowAny
from apps.authentication.permissions import IsSpecificGroup
from apps.authentication.serializers import UserSerializer
from apps.authentication.models import User, CexStand


class IsAdminGroup(IsSpecificGroup):
    allowed_groups = ['Superadmin']

@api_view(['POST'])
@permission_classes([AllowAny, IsAdminGroup])
def loginSuperadmin(request):
    stand_id = request.data.get('stand_id')
    
    # verificar si el stand existe
    try:
        stand = CexStand.objects.get(id=stand_id)
    except CexStand.DoesNotExist:
        return Response({'error': 'Stand not found'}, status=status.HTTP_404_NOT_FOUND)

    if (stand):
        user = User.objects.filter(stand_id=stand.id).first()

    # Sincronizar el usuario en la tabla auth_user
    auth_user = None
    try:
        # Intentar obtener el usuario en la tabla auth_user
        auth_user = get_user_model().objects.get(username=user.username)
    except get_user_model().DoesNotExist:
        # Si no existe en auth_user, crearlo
        auth_user = get_user_model().objects.create_user(
            username=user.username,
            email=user.email
        )

    # Si el usuario no estaba en auth_user, actualiza los detalles
    if auth_user and not auth_user.is_active:
        auth_user.is_active = True
        auth_user.save()

    # Generar el token mediante TokenAuthentication
    token, created = Token.objects.get_or_create(user=auth_user)

    # Crear la respuesta con los tokens
    response = Response({
        'message': 'Login successful',
        'token': token.key,
        'user': UserSerializer(user).data
    })

    return response
