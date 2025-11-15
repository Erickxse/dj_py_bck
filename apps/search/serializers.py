from rest_framework import serializers
from apps.category.models import CexCategory
from apps.stand.models import CexStand
from apps.service_product.models import CexServiceProduct
from apps.stand.models import CexCountry

class CexServiceProductSerializer(serializers.ModelSerializer):
    stand_slug = serializers.SerializerMethodField()
    stand_name = serializers.SerializerMethodField()
    stand_id = serializers.SerializerMethodField()
    slug_cat_3 = serializers.SerializerMethodField()
    slug_cat_2 = serializers.SerializerMethodField()
    slug_cat_1 = serializers.SerializerMethodField()
    name_cat_3 = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()

    class Meta:
        model = CexServiceProduct
        fields = ['id','name', 'slug', 'stand_slug', 'stand_name','stand_id', 'slug_cat_3', 'slug_cat_2', 'slug_cat_1', 'name_cat_3', 'price', 'images', 'country_name', 'type']

    def get_stand_slug(self, obj):
        # Obtén el stand correspondiente y devuelve su slug
        stand = CexStand.objects.filter(id=obj.stand_id).first()
        return stand.slug if stand else None

    def get_stand_name(self, obj):
        # Obtén el stand correspondiente y devuelve su stand_name
        stand = CexStand.objects.filter(id=obj.stand_id).first()
        return stand.stand_name if stand else None
    
    def get_stand_id(self, obj):
       # Return the stand_id directly from the object
        return obj.stand_id
    
    
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
        
    def get_slug_cat_2(self, obj):
        try:
            category = CexCategory.objects.get(id=obj.category_id)
            parent_category = CexCategory.objects.get(id=category.parent_id)
            return parent_category.slug
        except CexCategory.DoesNotExist:
            return None

    def get_slug_cat_1(self, obj):
        try:
            category = CexCategory.objects.get(id=obj.category_id)
            parent_category = CexCategory.objects.get(id=category.parent_id)
            grandparent_category = CexCategory.objects.get(id=parent_category.parent_id)
            return grandparent_category.slug
        except CexCategory.DoesNotExist:
            return None

    def get_country_name(self, obj):
        try:
            country = CexCountry.objects.get(id=obj.country_id)
            return country.name
        except CexCountry.DoesNotExist:
            return None  

        
class CexStandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CexStand
        fields = ['id','stand_name', 'slug','img']

class CexCategorySerializer(serializers.ModelSerializer):
    slug_cat_3 = serializers.SerializerMethodField()
    slug_cat_2 = serializers.SerializerMethodField()
    slug_cat_1 = serializers.SerializerMethodField()

    class Meta:
        model = CexCategory
        fields = ['id','name', 'slug', 'slug_cat_3', 'slug_cat_2', 'slug_cat_1','img']

    def get_slug_cat_3(self, obj):
        # Si el objeto ya es nivel 3, devolver su propio slug
        if obj.level == 3:
            return obj.slug
        # Si el objeto es nivel 2 o 1, devolver None
        return None

    def get_slug_cat_2(self, obj):
        try:
            # Si es nivel 3, buscar la categoría padre (nivel 2)
            if obj.level == 3:
                parent_category = CexCategory.objects.get(id=obj.parent_id)
                return parent_category.slug
            # Si es nivel 2, devolver su propio slug
            elif obj.level == 2:
                return obj.slug
            # Si es nivel 1, devolver None
            return None
        except CexCategory.DoesNotExist:
            return None

    def get_slug_cat_1(self, obj):
        try:
            # Si es nivel 3, buscar el abuelo (nivel 1)
            if obj.level == 3:
                parent_category = CexCategory.objects.get(id=obj.parent_id)
                grandparent_category = CexCategory.objects.get(id=parent_category.parent_id)
                return grandparent_category.slug
            # Si es nivel 2, buscar el padre (nivel 1)
            elif obj.level == 2:
                parent_category = CexCategory.objects.get(id=obj.parent_id)
                return parent_category.slug
            # Si es nivel 1, devolver su propio slug
            elif obj.level == 1:
                return obj.slug
            return None
        except CexCategory.DoesNotExist:
            return None