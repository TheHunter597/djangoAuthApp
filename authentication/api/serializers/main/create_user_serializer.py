from rest_framework import serializers
from ....models import UserModel


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = UserModel
        fields = ("email", "password", "confirm_password", "first_name", "last_name")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
            },
            "confirm_password": {
                "write_only": True,
                "min_length": 8,
            },
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "password": "passwords must match",
                    "confirm_password": "passwords must match",
                }
            )
        return super().validate(attrs)

    def validate_email(self, value):
        if UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists.")
        return value

    def save(self, **kwargs):
        self.validated_data.pop("confirm_password")
        user = UserModel.objects.create_user(**self.validated_data)
        return user
