from rest_framework import serializers
#from django.contrib.auth.models import User
from .models import User
from .models import AuthGroup

"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_active', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'required': False},  # Si lo quieres opcional
        }

    def create(self, validated_data):
        # Aquí se valida y se ajusta el password
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
"""

class UserSerializer(serializers.ModelSerializer):
    have_new_password = serializers.SerializerMethodField()
    role_name = serializers.SerializerMethodField()

    # Método para calcular el valor de have_new_password
    def get_have_new_password(self, obj):
        return obj.new_password is not None

    def get_role_name(self, obj):
        try:
            group = AuthGroup.objects.get(id=obj.role)
            return group.name
        except AuthGroup.DoesNotExist:
            return None

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'stand_id', 'is_complete',
                  'have_new_password', 'role_name', 'new_password')
