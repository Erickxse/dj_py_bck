from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
# from rest_framework_simplejwt.tokens import RefreshToken ->Ya no se usaría
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.authentication.permissions import IsSpecificGroup
from apps.authentication.serializers import UserSerializer
from apps.authentication.models import User, CexStand
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class IsAdminGroup(IsSpecificGroup):
    allowed_groups = ['Admin', 'Superadmin']


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminGroup])
def changePassword(request):
    # Obtener datos del request
    past_password = request.data.get('past_password')
    new_password = request.data.get('password')

    # Validar que se envíen los campos requeridos
    if not past_password or not new_password:
        return Response({
            'error': 'past_password y password son requeridos',
        }, status=status.HTTP_400_BAD_REQUEST)

    # Obtener el usuario autenticado desde el token
    auth_user = request.user

    # Buscar en la tabla `User` el usuario correspondiente
    try:
        user = User.objects.get(username=auth_user.username)
    except User.DoesNotExist:
        return Response({
            "error": "Usuario no encontrado en la base de datos"
        }, status=status.HTTP_404_NOT_FOUND)

    # Validar contraseña actual
    if not user.new_password:
        return Response({
            'error': 'El usuario no tiene contraseña configurada',
        }, status=status.HTTP_400_BAD_REQUEST)

    if not check_password(past_password, user.new_password):
        return Response({
            'message': 'La contraseña actual no es correcta',
        }, status=status.HTTP_400_BAD_REQUEST)

    # Actualizar contraseña en auth_user (Django)
    auth_user.password = make_password(new_password)
    auth_user.save()

    # Actualizar contraseña en tabla User personalizada
    hashed_password = make_password(new_password)
    user.new_password = hashed_password
    user.save()

    response = Response({
        'message': 'Contraseña actualizada correctamente',
        'user': UserSerializer(user).data,
    })

    return response

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminGroup])
def changePasswordSuperadmin(request):
    userId = request.data.get('userId')
    new_password = request.data.get('new_password')
    
    user = User.objects.filter(id=userId).first()

    auth_user = None
    try:
        auth_user = get_user_model().objects.get(username=user.username)
    except get_user_model().DoesNotExist:
        auth_user = get_user_model().objects.create_user(
            username=user.username,
            email=user.email
        )

    auth_user.password = make_password(new_password)
    auth_user.save()

    passw = user.new_password

    hashed_password = make_password(new_password)

    user.new_password = hashed_password
    user.save()

    response = Response({
        'message': 'Contraseña actualizada correctamente',
        'user': UserSerializer(user).data,
        'password': passw,
    })

    return response
