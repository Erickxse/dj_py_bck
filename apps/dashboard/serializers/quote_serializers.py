from rest_framework import serializers
from apps.dashboard.models import CexQuotes
from apps.service_product.models import CexServiceProduct
from apps.category.models import CexCategory
from apps.authentication.models import CexCountry, CexProvince


class CexQuoteSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = CexQuotes
        fields = ['quoted_by', 'quote_phone', 'product_name']

    def get_product_name(self, obj):
        try:
            product = CexServiceProduct.objects.get(id=obj.service_product_id)
            return product.name
        except CexServiceProduct.DoesNotExist:
            return None

# Nuevo serializador para el endpoint solicitado
class CexQuoteByStandSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = CexQuotes
        fields = ['id','status', 'quoted_by', 'quote_phone', 'product_name', 'category_name']

    def get_product_name(self, obj):
        try:
            product = CexServiceProduct.objects.get(id=obj.service_product_id)
            return product.name
        except CexServiceProduct.DoesNotExist:
            return None

    def get_category_name(self, obj):
        try:
            product = CexServiceProduct.objects.get(id=obj.service_product_id)
            category = CexCategory.objects.get(id=product.category_id)
            return category.name
        except (CexServiceProduct.DoesNotExist, CexCategory.DoesNotExist):
            return None
        
        
# Nuevo serializador para los detalles de los pedidos
class CexQuoteDetailsSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()
    province_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CexQuotes
        fields = ['quoted_by', 'quote_phone',
                  'quote_email', 'province_name', 'country_name',
                  'product_name', 'id', 'quoted_on', 'service_product_no_of_items', 
                  'status', 'quote_notes']

    def get_product_name(self, obj):
        try:
            product = CexServiceProduct.objects.get(id=obj.service_product_id)
            return product.name
        except CexServiceProduct.DoesNotExist:
            return None
        
    def get_country_name(self, obj):
        try:
            country = CexCountry.objects.get(id=obj.quote_country)
            return country.name
        except CexCountry.DoesNotExist:
            return None

    def get_province_name(self, obj):
        try:
            province = CexProvince.objects.get(id=obj.quote_province)
            return province.name
        except CexProvince.DoesNotExist:
            return None

