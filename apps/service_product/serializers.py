from rest_framework import serializers
from .models import CexServiceProduct
from apps.stand.models import CexStand
from apps.category.models import CexCategory
from apps.stand.models import CexCountry
import re

class CexServiceProductSerializer(serializers.ModelSerializer):
    stand_name = serializers.SerializerMethodField()
    stand_id = serializers.SerializerMethodField()
    stand_slug = serializers.SerializerMethodField()
    obras = serializers.SerializerMethodField()
    name_cat_3 = serializers.SerializerMethodField()
    category_id = serializers.IntegerField(read_only=True)  # Sin el source
    slug_cat_3 = serializers.SerializerMethodField()
    slug_cat_2 = serializers.SerializerMethodField()
    slug_cat_1 = serializers.SerializerMethodField()
    image_stand = serializers.SerializerMethodField()
    creation_date = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()

    class Meta:
        model = CexServiceProduct
        fields = ['id', 'slug', 'name', 'description', 'image', 'brand', 'specifications', 'price', 'images', 'stand_name', 'stand_id',
                  'stand_slug', 'obras', 'category_id', 'country', 'country_name', 'name_cat_3', 'slug_cat_1', 'slug_cat_2', 'slug_cat_3', 'image_stand', 
                  'creation_date', 'size', 'type']  # Agregado

    def get_stand_name(self, obj):
        # Obtener el stand correspondiente utilizando el stand_id
        stand = CexStand.objects.filter(id=obj.stand_id).first()
        return stand.stand_name if stand else None

    def get_stand_id(self, obj):
        stand = CexStand.objects.filter(id=obj.stand_id).first()
        return stand.id if stand else None
    
    def get_stand_slug(self, obj):
        stand = CexStand.objects.filter(id=obj.stand_id).first()
        return stand.slug if stand else None


    def get_obras(self, obj):
        # Contar cuántas obras coinciden con el stand_id
        return CexServiceProduct.objects.filter(stand_id=obj.stand_id).count()
    
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
        
    def get_image_stand(self, obj):
        try:
            # Obtener el stand correspondiente utilizando el stand_id
            stand = CexStand.objects.get(id=obj.stand_id)
            return stand.img
        except CexStand.DoesNotExist:
            return None

    def get_country_name(self, obj):
        try:
            country = CexCountry.objects.get(id=obj.country_id)
            return country.name
        except CexCountry.DoesNotExist:
            return None

    def get_creation_date(self, obj):
        return obj.creation_date.year if obj.creation_date else None   

    def get_size(self, obj):
        def extract_dimensions(text):
            text = text.lower()
            
            # Caso 1: detectar algo como "80 x 30 x 40 cm" o "80x30x40cm"
            match = re.search(r'(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)(?:\s*cm)?', text)
            if match:
                return f"{match.group(1)} cm x {match.group(2)} cm x {match.group(3)} cm"
            
            # Caso 2: al menos dos números seguidos de "cm"
            matches = re.findall(r'(\d+(?:\.\d+)?)\s*cm', text)
            if len(matches) >= 2:
                return f"{matches[0]} cm x {matches[1]} cm"

            # Caso 3: dimensiones sin unidad, como "24x36" o "24 x 36"
            match = re.search(r'(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)', text)
            if match:
                return f"{match.group(1)} cm x {match.group(2)} cm"

            return None

        # Intentar extraer de specifications
        size = extract_dimensions(obj.specifications or "")
        if size:
            return size

        # Si no se encontró nada, intentar con description
        return extract_dimensions(obj.description or "")



class CexServiceProductDataSerializer(serializers.ModelSerializer):
    stand_slug = serializers.SerializerMethodField()
    stand_name = serializers.SerializerMethodField()
    slug_cat_3 = serializers.SerializerMethodField()
    name_cat_3 = serializers.SerializerMethodField()
    slug_cat_2 = serializers.SerializerMethodField()
    slug_cat_1 = serializers.SerializerMethodField()
    obras = serializers.SerializerMethodField()
    image_stand = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        img_str = data.get('images')
        if isinstance(img_str, str):
            data['images'] = img_str.lstrip(',')
        return data
    
    class Meta:
        
        model = CexServiceProduct
        fields = ['id', 'name', 'category_id', 'description', 'obras', 'counter', 'slug', 'price', 'image', 'images', 'stand_slug',
                  'stand_id', 'stand_name', 'slug_cat_3', 'name_cat_3', 'slug_cat_2', 'slug_cat_1', 'country', 'image_stand', 'type']
     
    def get_stand_slug(self, obj):
        try:
            return CexStand.objects.get(id=obj.stand_id).slug
        except CexStand.DoesNotExist:
            return None
        
    def get_stand_name(self, obj):
        try:
            return CexStand.objects.get(id=obj.stand_id).stand_name
        except CexStand.DoesNotExist:
            return None

    def get_slug_cat_3(self, obj):
        try:
            category = CexCategory.objects.get(id=obj.category_id)
            return category.slug
        except CexCategory.DoesNotExist:
            return None
        
    def get_name_cat_3(self, obj):
        try:
            category = CexCategory.objects.get(id=obj.category_id)
            return category.name
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
    
    def get_obras(self, obj):
        # Contar cuántas obras coinciden con el stand_id
        return CexServiceProduct.objects.filter(stand_id=obj.stand_id).count()
    
    def get_image_stand(self, obj):
        try:
            # Obtener el stand correspondiente utilizando el stand_id
            stand = CexStand.objects.get(id=obj.stand_id)
            return stand.img
        except CexStand.DoesNotExist:
            return None
        
    def get_country(self, obj):
        try:
            return obj.country.name
        except CexCountry.DoesNotExist:
            return None
        

class CexCategoriesNamesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CexCategory
        fields = ['id', 'name']