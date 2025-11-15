from rest_framework import serializers
from .models import CexCategory
from apps.service_product.models import CexServiceProduct
from apps.stand.models import CexStand

class CategorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = CexCategory
        fields = '__all__'
        
        
class CategoryCarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = CexCategory
        fields = ['name', 'img','slug', 'description']
        

class DynamicChildrenSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255)
    img = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    level = serializers.IntegerField()
    parent_id = serializers.IntegerField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Añadir los hijos dinámicamente
        for key in instance.keys():
            if key.startswith('children_'):
                representation[key] = instance[key]
        return representation

class CategoryTreeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255)
    short_description = serializers.CharField(max_length=255)
    img = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    level = serializers.IntegerField()
    parent_id = serializers.IntegerField()
    slug = serializers.CharField(max_length=100)
    # No definimos children aquí

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Añadir los hijos dinámicamente
        for key in instance.keys():
            if key.startswith('children_'):
                representation[key] = instance[key]
        return representation

class CategorySubSerializerProd(serializers.ModelSerializer):
    stand_name = serializers.SerializerMethodField()  # Nuevo campo para stand_name

    class Meta:
        model = CexServiceProduct
        fields = ['id', 'slug', 'name', 'stand_name']  # Incluir stand_name

    # Método para obtener el nombre del stand
    def get_stand_name(self, obj):
        try:
            stand = CexStand.objects.get(id=obj.stand_id)  # Obtener el stand relacionado
            return stand.stand_name  # Devolver el nombre del stand
        except CexStand.DoesNotExist:
            return None  # Devolver None si no se encuentra el stand




