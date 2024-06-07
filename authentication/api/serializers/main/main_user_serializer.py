from rest_framework import serializers
from ....models import UserModel
from ..others.interest_serializer import InterestSerializer


class MainUserSerializer(serializers.ModelSerializer):
    interests = InterestSerializer(many=True)

    class Meta:
        model = UserModel
        fields = (
            "first_name",
            "last_name",
            "address",
            "email",
            "is_superuser",
            "is_staff",
            "city",
            "state",
            "country",
            "interests",
            "avatar",
            "is_active",
            "account_confirmed",
            "id",
            "phone_number",
            "zip_code",
            "date_joined",
        )
