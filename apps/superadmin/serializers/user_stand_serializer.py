from rest_framework import serializers

class UserStandInfoSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(allow_null=True)
    user_name = serializers.CharField(allow_null=True)
    stand_name = serializers.CharField(allow_null=True)
    role = serializers.CharField(allow_null=True)
    email = serializers.EmailField(allow_null=True)
