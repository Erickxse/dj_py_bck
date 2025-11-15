import os
from rest_framework import serializers
from .models import CexStand, CexPlan, CexSubscription, CexExhibition, Profile
from apps.authentication.models import CexCountry
from apps.service_product.models import CexServiceProduct

class CexStandSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    
    def get_code(self, obj):
        try:
            #obtener el codigo de la exhibicion relacionada al stand
            exhibition = CexExhibition.objects.get(stand_id=obj.id)
            return exhibition.code
        except CexExhibition.DoesNotExist:
            return None
        
    def get_city_name(self, obj):
        try:
            #obtener el nombre del pais relacionado al stand
            country = Profile.objects.get(user_id=obj.user_id)
            return country.cex_city
        except Profile.DoesNotExist:
            return None
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        raw = data.get('img')
        if raw:
            data['img'] = os.path.basename(raw)
        return data
    
    def get_country(self, obj):
        try:
            return obj.country.iso.lower()
        except AttributeError:
            return None
    
    class Meta:
        model = CexStand
        fields = ['id', 'stand_name', 'description',
                  'img', 'hits', 'pro_slide_image', 'code', 'tour_virtual_code', 'tour_virtual_active','city_name', 'created_at', 'country']


class CexStandListSerializer(serializers.ModelSerializer):

    plan_id = serializers.SerializerMethodField()
    imgs_obras = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()

    class Meta:
        model = CexStand
        fields = ['id', 'stand_name', 'slug', 'img',
                  'plan_id', 'country_name', 'imgs_obras', 'country']

    def get_isdeleted(self, obj):
        # Convertir bytes a booleano
        return obj.isdeleted == b'\x01'

    def get_isactive(self, obj):
        # Convertir bytes a booleano
        return obj.isactive == b'\x01'

    def get_plan_id(self, obj):
        # Obtener el plan activo
        subscription = CexSubscription.objects.filter(stand_id=obj.id).first()
        return subscription.plan_id if subscription else None

    def get_imgs_obras(self, obj):
        try:
            # Obtener hasta 4 imágenes más recientes del modelo CexServiceProduct ordenadas por creation_date
            products = (
                CexServiceProduct.objects
                .filter(stand_id=obj.id)
                .order_by('-creation_date')[:4]
                # Solo obtener el campo 'image'
                .values_list('image', flat=True)
            )
            # Convertir el queryset en una lista de strings (imágenes)
            return list(products)
        except Exception:
            return []

    def get_country(self, obj):
        try:
            country = CexCountry.objects.get(id=obj.country_id)
            return country.name
        except CexCountry.DoesNotExist:
            return None
    
    def get_country_name(self, obj):
        try:
            return obj.country.name
        except AttributeError:
            return None



class MostQuotedStandSerializer(serializers.Serializer):
    id=serializers.CharField()
    stand_name = serializers.CharField()
    slug = serializers.CharField()
    img = serializers.CharField(allow_null=True)
    works = serializers.IntegerField()
    
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CexPlan
        fields = ['id', 'name']
