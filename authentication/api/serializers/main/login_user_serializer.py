from rest_framework import serializers

from ....models import UserModel

class BasicUserDataSerializer(serializers.ModelSerializer):
    """login serializer for the user object"""
    class Meta:
        model = UserModel
        fields = ('email',"id")
    def validate(self, attrs):
        return super().validate(attrs)