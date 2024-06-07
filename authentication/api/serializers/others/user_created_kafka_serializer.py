from rest_framework import serializers

from ....models import UserModel

class UserCreatedKafkaSerializer(serializers.ModelSerializer):
    """login serializer for the user object"""
    class Meta:
        model = UserModel
        fields = ('email',"id","avatar","first_name","last_name","is_active")
    def validate(self, attrs):
        return super().validate(attrs)