from rest_framework import serializers
from ....models import UserModel


class ResetUserPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=128, write_only=True)
    confirm_new_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = UserModel
        fields = ("new_password", "confirm_new_password")

    def validate(self, attrs):
        if not attrs["new_password"] or not attrs["confirm_new_password"]:
            raise serializers.ValidationError(
                {
                    "message": "Password change error",
                    "errors": {
                        "new_password": ["New password wasnt provided"],
                        "confirm_new_password": ["Confirm new password wasnt provided"],
                    },
                }
            )

        if attrs["new_password"] != attrs["confirm_new_password"]:
            raise serializers.ValidationError(
                {
                    "message": "Password change error",
                    "errors": {
                        "new_password": [
                            "new password and confirm new password do not match"
                        ],
                        "confirm_new_password": [
                            "new password and confirm new password do not match"
                        ],
                    },
                }
            )
        return super().validate(attrs)
