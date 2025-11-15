from rest_framework import serializers
from apps.service_product.models import CexServiceProduct
from apps.stand.models import CexStand
from apps.category.models import CexCategory
from apps.stand.models import CexCountry

# Serializador para GET
class CexServiceProductGetSerializer(serializers.ModelSerializer):
    slug_cat_3 = serializers.SerializerMethodField()
    name_cat_3 = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()
    stand_slug = serializers.SerializerMethodField()
    stand_id = serializers.SerializerMethodField()
    product_slug = serializers.SerializerMethodField()
    country_code = serializers.SerializerMethodField()

    class Meta:
        model = CexServiceProduct
        fields = ['id', 'image', 'images', 'name', 'name_cat_3', 'slug_cat_3', 
                  'active', 'counter','stand_slug', 'stand_id', 'product_slug','price',
                  'description','country_code', 'type']

    def get_active(self, obj):
        return bool(obj.active)
    
    def get_name_cat_3(self, obj):
        try:
            category = CexCategory.objects.get(id=obj.category_id)
            return category.name
        except CexCategory.DoesNotExist:
            return None
        
    def get_slug_cat_3(self, obj):
        try:
            category = CexCategory.objects.get(id=obj.category_id)
            return category.slug
        except CexCategory.DoesNotExist:
            return None
        
    def get_stand_slug(self, obj):
        try:
            stand = CexStand.objects.get(id=obj.stand_id)
            return stand.slug
        except CexStand.DoesNotExist:
            return None
        
    def get_stand_id(self, obj):
        try:
            stand = CexStand.objects.get(id=obj.stand_id)
            return stand.id
        except CexStand.DoesNotExist:
            return None
        
    def get_product_slug(self, obj):
        return obj.slug
    
    def get_country_code(self, obj):
        try:
            country = CexCountry.objects.get(id=obj.country_id)
            return country.iso.lower()
        except CexCountry.DoesNotExist:
            return None

# Serializador para POST
class CexServiceProductPostSerializer(serializers.ModelSerializer):
    seo_id = serializers.IntegerField(allow_null=True, required=False)
    vr_tour = serializers.CharField(allow_blank=True)
    bnb_code = serializers.CharField(allow_blank=True)
    country_id = serializers.IntegerField()

    class Meta:
        model = CexServiceProduct
        fields = [
            'id', 'stand_id', 'category_id', 'seo_id', 'name', 'specifications', 'description',
            'type', 'upc', 'price', 'creation_date', 'image', 'images', 'slug',
            'vr_tour', 'bnb_code', 'country_id', 'counter', 'active'
        ]
        read_only_fields = ['id', 'counter', 'active','country_id']

    def validate(self, data):
        # Si es una actualización parcial (PUT), no validar campos obligatorios
        if self.partial:
            return data
        
        # Validaciones para creación (POST)
        required_fields = [
            'category_id', 'name', 'description',
            'price'
        ]
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError({field: f"El campo '{field}' es obligatorio"})

        valid_types = ['product', 'service']
        if data.get('type') not in valid_types:
            raise serializers.ValidationError({"type": f"El campo 'type' debe ser uno de {valid_types}"})

        # Asegurar que active sea True por defecto si no está presente
        if 'active' not in data:
            data['active'] = True

        return data
