from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.dashboard.views.Group import IsAdminGroup
from apps.stand.models import CexPlan, CexSubscription, CexStand
from apps.dashboard.models import Profile
from apps.dashboard.serializers.profile_serializers import ProfileSerializer, ProfileUpdateSerializer
from apps.authentication.models import User

class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminGroup]

    def get(self, request):
        # Obtener el usuario autenticado desde el token
        auth_user = request.user

        # Buscar en la tabla `User` el usuario correspondiente
        try:
            user = User.objects.get(username=auth_user.username)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado en la base de datos"}, status=404)

        # Verificar si el usuario tiene un `stand_id`
        if not user.stand_id:
            return Response({"error": "El usuario no tiene un stand asignado"}, status=400)

        stand_id = user.stand_id

        # Buscar el stand del usuario
        stand = CexStand.objects.filter(id=stand_id).first()
        if not stand:
            return Response({"error": "No se encontró el stand asociado"}, status=404)

        # Buscar la suscripción activa usando `stand_id`
        subscription = CexSubscription.objects.filter(stand_id=stand_id, active=1).first()
        
        # No devolvemos un error 404, ya que queremos continuar mostrando el perfil
        if subscription:
            plan = CexPlan.objects.filter(id=subscription.plan_id).first()
        else:
            plan = None  # Si no hay suscripción, pasamos plan como None
   

        profile = Profile.objects.filter(user_id=user.id).first()

        # Serializar el plan usando ProfileSerializer, pasando la suscripción y el usuario al contexto
        serialized_data = ProfileSerializer(
            profile,
            context={
                "subscription": subscription,
                "stand": stand,
                "user": user,
                "plan" : plan,  # Pasamos el usuario al contexto
            },
        ).data

        return Response(serialized_data, status=200)

    def put(self, request):
        """ Actualiza `name` en Profile y `email` en User """
        auth_user = request.user

        # ✅ Buscar el usuario
        try:
            user = User.objects.get(username=auth_user.username)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=404)

        # ✅ Buscar el perfil asociado
        profile = Profile.objects.filter(user_id=user.id).first()
        if not profile:
            return Response({"error": "Perfil no encontrado"}, status=404)
        
        stand = CexStand.objects.filter(id=user.stand_id).first()
        if not stand:
            return Response({"error": "No se encontró el stand asociado"}, status=404)

        updated_data = request.data.copy()
        updated_data.pop("terms_and_conditions", None)  # Excluir términos si existen

        # ✅ Pasamos `profile` al serializer, que también actualizará `user`
        serializer = ProfileUpdateSerializer(profile, data=updated_data, partial=True)

        if serializer.is_valid():
            serializer.save()  # ✅ Guarda `name` en `Profile` y `email` en `User`
            return Response({"message": "Perfil actualizado correctamente", "data": serializer.data}, status=200)

        return Response(serializer.errors, status=400)




