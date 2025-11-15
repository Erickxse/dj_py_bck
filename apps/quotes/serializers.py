from rest_framework import serializers
from .models import CexQuotes
from datetime import datetime

class CexQuotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CexQuotes
        fields = [
            'stand_id', 
            'service_product_id',
            'quoted_by',
            'quote_email',
            'quote_phone',
            'quote_notes',
            'service_product_no_of_items',
            'quote_country',
            'quote_province', 
        ]
    
    def create(self, validated_data):
        # Valores por defecto que coincidan con los ENUMs de la BD
        validated_data.update({
            'status': 'nuevo',
            'ispaid': 0,
            'quoted_on': datetime.now(),
            'quote_preferred_contact': 'Email',  # Exactamente como está en el ENUM
            'quote_price': 0,
            'quote_created': datetime.now(),
            'quote_type': 'quote',  # Valor válido del ENUM
            'payed': 0,
            # Asegurar otros campos requeridos
            'quote_c1': validated_data.get('quote_c1', 0),
            'quote_c2': validated_data.get('quote_c2', 0),
            'quote_c3': validated_data.get('quote_c3', 0),
        })
        
        return super().create(validated_data)