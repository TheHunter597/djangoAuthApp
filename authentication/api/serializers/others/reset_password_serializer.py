from rest_framework import serializers
from ....models import UserModel


class ResetUserPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=128, write_only=True)
    confirm_new_password = serializers.CharField(max_length=128, write_only=True)
    email = serializers.CharField(max_length=128, write_only=True)
    confirmation_token = serializers.CharField(max_length=256, write_only=True)

    class Meta:
        model = UserModel
        fields = ("new_password", "confirm_new_password", "email", "confirmation_token")

    def validate(self, attrs):
        if not attrs["new_password"] or not attrs["confirm_new_password"]:
            raise serializers.ValidationError(
                {
                    "new_password": ["New password wasnt provided"],
                    "confirm_new_password": ["Confirm new password wasnt provided"],
                }
            )

        if attrs["new_password"] != attrs["confirm_new_password"]:
            raise serializers.ValidationError(
                {
                    "new_password": [
                        "New password and confirm new password do not match"
                    ],
                    "confirm_new_password": [
                        "New password and confirm new password do not match"
                    ],
                }
            )
        if len(attrs["new_password"]) < 8:
            raise serializers.ValidationError(
                {
                    "new_password": [
                        "Password must be at least 8 characters long",
                    ]
                }
            )
        try:
            user = UserModel.objects.filter(email=attrs["email"]).first()
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "message": "Invalid token",
                    "errors": {"token": "The token provided is invalid"},
                }
            )

        if user.activation_token != attrs["confirmation_token"]:
            raise serializers.ValidationError(
                {
                    "message": "Invalid token",
                    "errors": {"token": "The token provided is invalid"},
                }
            )
        return super().validate(attrs)

    def save(self, **kwargs):
        return UserModel.objects.filter(email=self.validated_data["email"]).first()
