import base64
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
#from rest_framework_simplejwt.tokens import RefreshToken ->Ya no se usaría
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from apps.authentication.utils import enviarCorreo, enviarCorreoResetPass
from .models import User, AxUserOtp, CexCountry, CexProvince, CexStand, Profile, CexSubscription
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta
from django.db import transaction, IntegrityError
from django.core.cache import cache
import random
import string
from django.utils import timezone


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # Obtener las credenciales enviadas en el body
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "Invalid username"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if user.new_password:
        if not check_password(password, user.new_password):
            return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"message": "Debes reiniciar la contraseña"}, status=status.HTTP_202_ACCEPTED)    
    
    # Sincronizar el usuario en la tabla auth_user
    auth_user = None
    try:
        # Intentar obtener el usuario en la tabla auth_user
        auth_user = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        # Si no existe en auth_user, crearlo
        auth_user = get_user_model().objects.create_user(
            username=username,
            password=user.new_password,  # Guardar la contraseña cifrada
            email=user.email
        )
    
    # Si el usuario no estaba en auth_user, actualiza los detalles
    if auth_user and not auth_user.is_active:
        auth_user.is_active = True
        auth_user.save()
    
    #Generar el token mediante TokenAuthentication
    token, created = Token.objects.get_or_create(user=auth_user)
    
    # Crear la respuesta con los tokens
    response = Response({
        'message': 'Login successful',
        'token': token.key, 
        'user': UserSerializer(user).data
    })
    
    return response

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Validaciones básicas
    if not email or not password:
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    # desencriptar la contraseña de base64
    password = base64.b64decode(password).decode('utf-8')

    # Crear el usuario con contraseña hasheada
    hashed_password = make_password(password)  # Hasheando la contraseña
    user = User.objects.create(
        username=email,
        email=email,
        password_hash="passwordhashed",
        # ==================================================================================================================================
        # Cambiar el campo de password cuando ya este en produccion.
        # ==================================================================================================================================
        new_password=hashed_password,
        created_at=int(datetime.now().timestamp()),
        updated_at=int(datetime.now().timestamp()),
        terms_and_conditions=True,
        country_id=66,
        role=2
    )
    
    return Response({
        "message": "User registered successfully",
        "user": UserSerializer(user).data
    }, status=status.HTTP_201_CREATED)

#view para el OPT
@api_view(['POST'])
@permission_classes([AllowAny])
def enviarOTP(request):
    email = request.data.get('email')
    isRegister = request.data.get('isRegister')

    if not email:
        return Response({"error": "Es necesario el correo."}, status=status.HTTP_400_BAD_REQUEST)
    
    if isRegister:
        if User.objects.filter(email=email).exists():
            return Response({"error": "El correo ya existe"}, status=status.HTTP_400_BAD_REQUEST)

    # Verificar si ya existe un OTP registrado para el email
    otp_record = AxUserOtp.objects.filter(email=email).first()

    if otp_record:
        # Verificar si ya expiro el codigo
        if otp_record.expires_at < timezone.now():
            # Si ha expirado, generar un nuevo OTP
            otp = ''.join(random.choices(string.digits, k=6))
            otp_record.otp = otp
            otp_record.created_at = timezone.now()
            otp_record.expires_at = timezone.now() + timedelta(seconds=300)  # 5 minutos más
            otp_record.save()

            # Almacenar el OTP en caché (se sobrescribe en caso de actualización)
            cache.set(f"otp_{email}", otp, timeout=300)

            if isRegister:
                # Enviar el OTP por correo electrónico
                enviarCorreo(email, otp)
            else:
                enviarCorreoResetPass(email, otp)

            # Devolver la hora de expiracion
            return Response({"message": "OTP sent successfully", "expires_at": otp_record.expires_at, "email": email}, status=status.HTTP_200_OK)
        else:
            # Consulta el tiempo de expiracion del otp
            return Response({"message": "OTP sent successfully", "expires_at": otp_record.expires_at, "email": email}, status=status.HTTP_200_OK)

    else:
        # Si el email no tiene un OTP registrado, crearlo
        otp = ''.join(random.choices(string.digits, k=6))
        newOtp = AxUserOtp.objects.create(
            email=email,
            otp=otp,
            created_at=timezone.now(),
            expires_at=timezone.now() + timedelta(seconds=300),
        )

        # Almacenar el OTP en caché (se sobrescribe en caso de actualización)
        cache.set(f"otp_{email}", otp, timeout=300)

        # Enviar el OTP por correo electrónico
        enviarCorreo(email, otp)

    return Response({"message": "OTP sent successfully", "expires_at": newOtp.expires_at, "email": newOtp.email}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def validarOTP(request):
    email = request.data.get('email')
    otp = request.data.get('otp')

    if not email or not otp:
        return Response({"error": "Email and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

    otp_record = AxUserOtp.objects.filter(email=email).first()

    if not otp_record:
        return Response({"error": "El OTP expiro o no fue generado."}, status=status.HTTP_400_BAD_REQUEST)

    if otp_record.otp == otp:
        return Response({"message": "Código OPT Correcto"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "OTP Invalido"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def resendOTP(request):
    email = request.data.get('email')
    isRegister = request.data.get('isRegister')
    otp_record = AxUserOtp.objects.filter(email=email).first()
    
    otp = ''.join(random.choices(string.digits, k=6))
    otp_record.otp = otp
    otp_record.created_at = timezone.now()
    otp_record.expires_at = timezone.now() + timedelta(seconds=300)  # 5 minutos más
    otp_record.save()

    # Almacenar el OTP en caché (se sobrescribe en caso de actualización)
    cache.set(f"otp_{email}", otp, timeout=300)

    if isRegister:
        # Enviar el OTP por correo electrónico
        enviarCorreo(email, otp)
    else:
        enviarCorreoResetPass(email, otp)

    # Devolver la hora de expiracion
    return Response({"message": "OTP sent successfully", "expires_at": otp_record.expires_at, "email": email}, status=status.HTTP_200_OK)


# ==================================================================================================================================
# ONBOARDING
# ==================================================================================================================================

# Enpoint para el pais
@api_view(['GET'])
@permission_classes([AllowAny])
def getCountry(request):
    # Obtener todos los países y extraer solo los nombres
    countries = CexCountry.objects.all().values_list('name', flat=True)
    countries_id = CexCountry.objects.all().values_list('id', flat=True)
    countries_iso = CexCountry.objects.all().values_list('iso', flat=True)
    return Response({"country": list(countries), "country_id": list(countries_id), "country_iso": list(countries_iso)}, status=status.HTTP_200_OK)

# Enpoint para la provincia
@api_view(['POST'])
@permission_classes([AllowAny])
def getProvince(request):
    idCountry = request.data.get('country')
    
    province = CexProvince.objects.filter(
        country_id=idCountry).values_list('name', flat=True)
    province_id = CexProvince.objects.filter(
        country_id=idCountry).values_list('id', flat=True)
    return Response({"provinces": list(province), "provices_id": list(province_id)}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic
def onboarding(request):
    profile = request.data.get('profile')
    stand = request.data.get('stand')

    email = profile.get('public_email')

    user = User.objects.filter(email=email).first()
    if not user:
        return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    # ------------------------------------------------
    # validar que el perfil, stand no existan con ese email
    # ------------------------------------------------
    
    if Profile.objects.filter(public_email=email).exists():
        return Response({"error": f"El perfil ya existe relacionado al correo {email}"}, status=status.HTTP_400_BAD_REQUEST)

    # Obtener id provincia
    province = profile.get('province')
    province_obj = CexProvince.objects.filter(name=province).first()
    if not province_obj:
        return Response({"error": f"Province {province} not found."}, status=status.HTTP_400_BAD_REQUEST)
    province_id = province_obj.id

    # Obtener el iso del country
    isoCountry = CexCountry.objects.filter(
        id=stand.get('country')).first()
    if not isoCountry:
        return Response({"error": f"Country {stand.get('country')} not found."}, status=status.HTTP_400_BAD_REQUEST)

    # obtener el slug
    #----------------------------------------------------------------------
    # Revisar
    #----------------------------------------------------------------------
    slug = stand.get('slug')
    if CexStand.objects.filter(slug=slug).exists():
        return Response({"error": "El slug ya existe"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():
            # Crear el perfil
            newProfile = Profile.objects.create(
                user_id=user.id,
                name=profile.get('name'),
                cex_first_name=profile.get('first_name'),
                cex_last_name=profile.get('last_name'),
                public_email=profile.get('public_email'),
                cex_contact_phone=profile.get('cex_contact_phone'),
                cex_city=profile.get('cex_city'),
                cex_country_id=profile.get('country'),
                cex_province_id=province_id,
                cex_contact_home_phone=profile.get('cex_contact_phone'),
                cex_status="nuevo",
                email_visitor_sent=0,
                location=isoCountry.iso,
                timezone="America/Guayaquil",
                
            )
            print(f"Perfil creado: {newProfile}")

            # Crear el stand
            newStand = CexStand.objects.create(
                user_id=user.id,
                stand_type_id=1,
                seo_id=stand.get('seo_id'),
                stand_name=stand.get('stand_name'),
                description=stand.get('description'),
                isactive=True,
                isdeleted=False,
                issleep=True,
                slug=stand.get('slug'),
                state_10=stand.get('state_10'),
                email=stand.get('email'),
                phone=stand.get('phone'),
                cex_whatsapp_phone=stand.get('phone'),
                country_id=stand.get('country'),
                credits_total=0,
                credits_extra=0,
                delivery_cost = 0,
                percent_price_contruex=0,
                percent_price_public_sale=0,
            )
            print(f"Stand creado: {newStand}")

            # Actualizar el estado del user
            user.is_complete = True
            user.stand_id = newStand.id
            # pasar a int antes de guardar
            user.country_id = int(newStand.country_id)
            user.save()

            # Crear la suscripción
            newSubscription = CexSubscription.objects.create(
                creation_date=timezone.localdate(),
                active=True,
                stand_id=newStand.id,
                plan_id=1,
                edit_user=user.id,
                plan_valid_for=365,
                months=12,
            )
            print("Suscripción creada")

            # Si todo salió bien
            print("Onboarding exitoso")
            return Response({"message": "Perfil creado correctamente"}, status=status.HTTP_200_OK)
        
    except IntegrityError as e:
        print(f"Error en la transacción: {e}")

        # Revertir cambios solo si los objetos fueron creados
        if 'newProfile' in locals():
            newProfile.delete()
        if 'newStand' in locals():
            newStand.delete()
        if 'newSubscription' in locals():
            newSubscription.delete()

        user.is_complete = False
        user.country_id = 0
        user.save()
        return Response({"error": "Error en la transacción, por favor intente nuevamente"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print(f"Error desconocido: {e}")

        # Revertir cambios solo si los objetos fueron creados
        if 'newProfile' in locals():
            newProfile.delete()
        if 'newStand' in locals():
            newStand.delete()
        if 'newSubscription' in locals():
            newSubscription.delete()

        user.is_complete = False
        user.country_id = 0
        user.save()
        return Response({"error": "Hubo un error, por favor intente nuevamente"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================================================================================================================================
# Endpoint para cambiar la contraseña
# ==================================================================================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def updatePassword(request):
    email = request.data.get('email')
    password = request.data.get('newPassword')

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(email=email).first()
    if not user:
        return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

    hashed_password = make_password(password)
    user.new_password = hashed_password
    user.save()

    return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

#validar el email en la base de datos
@api_view(['POST'])
@permission_classes([AllowAny])
def validarEmail(request):
    email = request.data.get('email')

    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(email=email).first()
    if user:
        return Response({"message": "El correo existe"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "El correo no existe"}, status=status.HTTP_400_BAD_REQUEST)
