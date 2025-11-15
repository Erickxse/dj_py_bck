from rest_framework import serializers
from apps.stand.models import CexPlan, CexStand
from apps.dashboard.models import Profile
from apps.authentication.models import User
from apps.dashboard.models import CexQuotes
from apps.authentication.models import CexProvince, CexCountry



class ProfileSerializer(serializers.ModelSerializer):
    stand_id = serializers.SerializerMethodField() 
    actual_plan = serializers.SerializerMethodField()  
    activation_date = serializers.SerializerMethodField() 
    description = serializers.SerializerMethodField()  
    email = serializers.SerializerMethodField()  
    username = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    stand_name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField() 
    phone = serializers.SerializerMethodField()
    date_first_quote = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    stand_slug = serializers.SerializerMethodField()
    country_code = serializers.SerializerMethodField() 

    class Meta:
        model = Profile
        fields = ["stand_id", "actual_plan", "activation_date", "description", "email", "username", "name", "stand_name", "image_url","phone","date_first_quote","location","stand_slug","country_code"]  # Agregamos email
    
    def get_actual_plan(self, obj):
        """
        Obtiene el nombre del plan desde el objeto CexPlan, o "N/A" si no hay plan.
        """
        plan = self.context.get("plan")
        return plan.name if plan else None  # Retorna el nombre del plan si existe, de lo contrario "N/A"


    def get_activation_date(self, obj):
        """
        Obtiene la fecha de activación desde la suscripción activa pasada en el contexto.
        """
        subscription = self.context.get("subscription")  # Extrae la suscripción del contexto
        if subscription:
            return subscription.creation_date  # Retorna la fecha si la suscripción existe
        return None

    def get_description(self, obj):
        """
        Obtiene la descripción desde el stand asociado, usando el stand_id en el contexto.
        """
        stand = self.context.get("stand")  # Extrae el stand del contexto
        if stand:
            return stand.description  # Retorna la descripción si el stand existe
        return None  # Si no hay stand, devuelve None

    def get_email(self, obj):
        """
        Obtiene el email desde el usuario autenticado, usando el contexto.
        """
        user = self.context.get("user")  # Extrae el usuario del contexto
        if user:
            return user.email  # Retorna el email del usuario
        return None  # Si no hay usuario, devuelve None
    
    def get_username(self, obj):
        """
        Obtiene el username desde el usuario autenticado, usando el contexto.
        """
        user = self.context.get("user")
        if user:
            return user.username
        return None
    
    def get_name(self, obj):
        """ Obtiene el campo `name` desde el modelo Profile asociado al usuario """
        user = self.context.get("user")
        if user:
            profile = Profile.objects.filter(user_id=user.id).first()
            return profile.name if profile else None  # Retorna el nombre si existe
        return None
    
    def get_phone(self, obj):
        """ Obtiene el telefono del contacto desde el modelo Profile asociado al usuario """
        user = self.context.get("user")
        if user:
            profile = Profile.objects.filter(user_id=user.id).first()
            return profile.cex_contact_phone if profile else None
    
    def get_date_first_quote(self, obj):
        """ Obtiene la fecha de la primera cotización (sin hora) """
        stand = self.context.get("stand")
        if stand:
            first_quote = CexQuotes.objects.filter(stand_id=stand.id).order_by("quoted_on").first()
            if first_quote:
                return first_quote.quoted_on.date()  # Retorna solo la fecha
        return None  # Si no hay cotizaciones, devuelve None
    
    def get_location(self, obj):
        """ Obtiene la ubicación del perfil en formato 'Provincia, Ciudad' """
        user = self.context.get("user")
        if user:
            profile = Profile.objects.filter(user_id=user.id).values("cex_province_id", "cex_city").first()
        if profile:
            province_name = (
                CexProvince.objects.filter(id=profile["cex_province_id"])
                .values_list("name", flat=True)
                .first()
                or "Desconocido"
            )
            city_name = profile["cex_city"] or "Desconocido"
            return f"{province_name}, {city_name}"
        return None
    
    
    def get_country_code(self, obj):
        """ Obtiene el código de país en minúsculas basado en el stand asociado al usuario """
        user = self.context.get("user")
        if user:
            stand_id = user.stand_id
            if stand_id:
                country_id = (
                    CexStand.objects.filter(id=stand_id)
                    .values_list("country_id", flat=True)
                    .first()
                )
                if country_id:
                    return (
                        CexCountry.objects.filter(id=country_id)
                        .values_list("iso", flat=True)
                        .first()
                        or None
                    ).lower()
        return None

    def get_stand_name(self, obj):
        """ Obtiene el `stand_name` desde el modelo CexStand """
        stand = self.context.get("stand")
        return stand.stand_name if stand else None
    
    def get_image_url(self, obj):
        """ Obtiene la URL de la imagen desde el modelo CexStand """
        stand = self.context.get("stand")
        return stand.img if stand else None  
    
    def get_stand_id(self, obj):
        """ Obtiene el ID del stand desde el modelo CexStand """
        stand = self.context.get("stand")
        return stand.id if stand else None
    
    def get_stand_slug(self, obj):
        """ Obtiene el slug del stand desde el modelo CexStand """
        stand = self.context.get("stand")
        return stand.slug if stand else None

class ProfileUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=False,
        min_length=2,
        max_length=100,
        error_messages={
            "min_length": "El nombre debe tener al menos 2 caracteres.",
            "max_length": "El nombre no puede superar los 100 caracteres.",
        },
    )
    email = serializers.EmailField(
        required=False,
        error_messages={"invalid": "El correo electrónico ingresado no es válido."},
    )
    stand_name = serializers.CharField(required=False, allow_blank=True, max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        """
        ✅ Verifica que el email no esté en uso por otro usuario antes de actualizarlo.
        """
        user = User.objects.get(id=self.instance.user_id)  # ✅ Obtener usuario desde el `user_id` en Profile

        # Si el email ya está en uso por otro usuario, se rechaza
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Este email ya está en uso por otro usuario.")

        return value  # ✅ Retorna el email si es válido

    def update(self, instance, validated_data):
        """
        `instance` es un `Profile`, pero también actualizaremos el `User` relacionado.
        """
        user = User.objects.get(id=instance.user_id)  # Obtener el usuario relacionado
        stand = CexStand.objects.get(id=user.stand_id)  # Obtener el stand del usuario

        # Si se envió un nuevo `name`, se actualiza en `Profile`
        if "name" in validated_data:
            instance.name = validated_data["name"]
            instance.save()

        # Si se envió un nuevo `email`, se actualiza en `User` y `Profile`
        if "email" in validated_data:
            new_email = validated_data["email"]
            user.email = new_email  # Actualiza el email en User
            user.username = new_email  # También actualiza el username en User
            user.save()
            instance.public_email = new_email  # ✅ Actualiza el public_email en Profile
            instance.save()

        # Si se envió un nuevo `stand_name`, se actualiza en `CexStand`
        if "stand_name" in validated_data:
            stand.stand_name = validated_data["stand_name"]
            stand.save()

        # Si se envió un nuevo `description`, se actualiza en `CexStand`
        if "description" in validated_data:
            stand.description = validated_data["description"]
            stand.save()

        return instance

