from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.authentication.models import CexCountry, CexProvince, CexSubscription, Profile, User, CexStand
from apps.superadmin.views.group import IsSuperAdminGroup
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import base64


class CreateStandView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdminGroup]
    
    def post(self, request):   
        try:
            data = request.data
            profile = data.get('profile')
            stand = data.get('stand')
            email = profile.get('public_email')
            password = data.get('password')

            # Validaciones básicas
            if not email or not password:
                return Response({"error": "Email y password son requeridos"}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({"error": "El email ya existe"}, status=status.HTTP_400_BAD_REQUEST)
            if Profile.objects.filter(public_email=email).exists():
                return Response({"error": f"El perfil ya existe relacionado al correo {email}"}, status=status.HTTP_400_BAD_REQUEST)
            slug = stand.get('slug')
            if CexStand.objects.filter(slug=slug).exists():
                return Response({"error": "El slug ya existe"}, status=status.HTTP_400_BAD_REQUEST)

           # Obtener provincia y país
            province = profile.get('province')
            province_id = 0
            if province and province != "N/A":
                province_obj = CexProvince.objects.filter(id=province).first()
                if not province_obj:
                    return Response({"error": f"Province {province} not found."}, status=status.HTTP_400_BAD_REQUEST)
                province_id = province_obj.id

            isoCountry = CexCountry.objects.filter(id=stand.get('country')).first()
            if not isoCountry:
                return Response({"error": f"Country {stand.get('country')} not found."}, status=status.HTTP_400_BAD_REQUEST)

            # Desencriptar y hashear password
            password = base64.b64decode(password).decode('utf-8')
            hashed_password = make_password(password)

            # Validar tour_virtual_active y tour_virtual_code
            tour_virtual_active = stand.get('tour_virtual_active', 0)
            try:
                tour_virtual_active = int(tour_virtual_active)
            except Exception:
                tour_virtual_active = 0
            tour_virtual_code = stand.get('tour_virtual_code', None)
            if tour_virtual_active == 1 and not tour_virtual_code:
                return Response({"error": "tour_virtual_code es obligatorio cuando tour_virtual_active es 1"}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                # Crear usuario
                user = User.objects.create(
                    username=email,
                    email=email,
                    password_hash="passwordhashed",
                    new_password=hashed_password,
                    created_at=int(timezone.now().timestamp()),
                    updated_at=int(timezone.now().timestamp()),
                    terms_and_conditions=True,
                    country_id=isoCountry.id,
                    role=2,
                    is_complete=False
                )
                print(f"Usuario creado: {user.username} con ID: {user.id}")

                # Crear perfil
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
                print(f"Perfil creado para el usuario: {user.username}")

                # Crear stand
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
                    delivery_cost=0,
                    percent_price_contruex=0,
                    percent_price_public_sale=0,
                    tour_virtual_active=tour_virtual_active,
                    tour_virtual_code=tour_virtual_code if tour_virtual_active == 1 else None,
                )
                print(f"Stand creado: {newStand.stand_name}")

                # Actualizar user
                user.is_complete = True
                user.stand_id = newStand.id
                user.country_id = int(newStand.country_id)
                user.save()

                # Crear suscripción
                newSubscription = CexSubscription.objects.create(
                    creation_date=timezone.localdate(),
                    active=True,
                    stand_id=newStand.id,
                    plan_id=1,
                    edit_user=user.id,
                    plan_valid_for=365,
                    months=12,
                )
                print(f"Suscripción creada para el stand: {newStand.stand_name}")

                return Response({"message": "Artista creado correctamente"}, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            print(f"Error en la transacción: {e}")
            if 'user' in locals():
                user.delete()
            if 'newProfile' in locals():
                newProfile.delete()
            if 'newStand' in locals():
                newStand.delete()
            if 'newSubscription' in locals():
                newSubscription.delete()
            return Response({"error": "Error en la transacción, por favor intente nuevamente"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f"Error en la transacción: {e}")
            if 'user' in locals():
                user.delete()
            if 'newProfile' in locals():
                newProfile.delete()
            if 'newStand' in locals():
                newStand.delete()
            if 'newSubscription' in locals():
                newSubscription.delete()
            return Response({"error": f"Error desconocido: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateStandView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdminGroup]

    def put(self, request, id):
        try:
            data = request.data
            profile = data.get('profile', {})
            stand = data.get('stand', {})
            password1 = data.get('password1', '')
            password2 = data.get('password2', '')

            # Buscar el stand y usuario
            try:
                stand_obj = CexStand.objects.get(id=id)
                user = User.objects.get(id=stand_obj.user_id)
                profile_obj = Profile.objects.get(user_id=user.id)
            except (CexStand.DoesNotExist, User.DoesNotExist, Profile.DoesNotExist):
                return Response({"error": "Stand, usuario o perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            # Validar cambio de contraseña
            if password1 and password2:
                if password1 != password2:
                    return Response({"error": "Las contraseñas no coinciden"}, status=status.HTTP_400_BAD_REQUEST)
                password_decoded = base64.b64decode(password1).decode('utf-8')
                hashed_password = make_password(password_decoded)
            else:
                hashed_password = None

            # Validar tour_virtual_active y tour_virtual_code
            tour_virtual_active = stand.get('tour_virtual_active', stand_obj.tour_virtual_active)
            try:
                tour_virtual_active = int(tour_virtual_active)
            except Exception:
                tour_virtual_active = 0
            tour_virtual_code = stand.get('tour_virtual_code', stand_obj.tour_virtual_code)
            if tour_virtual_active == 1 and not tour_virtual_code:
                return Response({"error": "tour_virtual_code es obligatorio cuando tour_virtual_active es 1"}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                # Actualizar usuario
                if hashed_password:
                    user.new_password = hashed_password
                user.email = profile.get('public_email', user.email)
                user.save()

                # Actualizar perfil
                profile_obj.name = profile.get('name', profile_obj.name)
                profile_obj.cex_first_name = profile.get('first_name', profile_obj.cex_first_name)
                profile_obj.cex_last_name = profile.get('last_name', profile_obj.cex_last_name)
                profile_obj.public_email = profile.get('public_email', profile_obj.public_email)
                profile_obj.cex_contact_phone = profile.get('cex_contact_phone', profile_obj.cex_contact_phone)
                profile_obj.cex_city = profile.get('cex_city', profile_obj.cex_city)
                profile_obj.cex_country_id = profile.get('country', profile_obj.cex_country_id)
                
                
                # Aquí corregimos para manejar correctamente "N/A"
                province = profile.get('province')
                if province == "N/A" or not province:
                    profile_obj.cex_province_id = None
                else:
                    profile_obj.cex_province_id = int(province)
                profile_obj.cex_contact_home_phone = profile.get('cex_contact_phone', profile_obj.cex_contact_home_phone)
                profile_obj.save()

                # Actualizar stand
                stand_obj.stand_name = stand.get('stand_name', stand_obj.stand_name)
                stand_obj.description = stand.get('description', stand_obj.description)
                stand_obj.slug = stand.get('slug', stand_obj.slug)
                stand_obj.state_10 = stand.get('state_10', stand_obj.state_10)
                stand_obj.email = stand.get('email', stand_obj.email)
                stand_obj.phone = stand.get('phone', stand_obj.phone)
                stand_obj.cex_whatsapp_phone = stand.get('phone', stand_obj.cex_whatsapp_phone)
                stand_obj.country_id = stand.get('country', stand_obj.country_id)
                stand_obj.tour_virtual_active = tour_virtual_active
                if 'tour_virtual_code' in stand:
                    stand_obj.tour_virtual_code = tour_virtual_code if tour_virtual_active == 1 else stand_obj.tour_virtual_code
                stand_obj.save()

                return Response({"message": "Stand actualizado correctamente"}, status=status.HTTP_200_OK)

        except IntegrityError as e:
            return Response({"error": "Error en la transacción, por favor intente nuevamente"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"Error desconocido: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)