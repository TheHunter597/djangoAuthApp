from rest_framework.views import APIView
from rest_framework import status
from .....models import UserModel
from ....serializers.others.reset_password_serializer import ResetUserPasswordSerializer
from rest_framework.response import Response
from rest_framework import serializers


class ChangePassword(APIView):
    """Reset user password"""

    def put(self, request):
        email = request.data.get("email")
        confirmation_token = request.data.get("confirmation_token")
        new_password = request.data.get("new_password")
        confirm_new_password = request.data.get("confirm_new_password")
        try:
            user = UserModel.objects.filter(email=email).first()
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "message": "Invalid token",
                    "errors": {"token": "The token provided is invalid"},
                }
            )
        if user.activation_token != confirmation_token:
            raise serializers.ValidationError(
                {
                    "message": "Invalid token",
                    "errors": {"token": "The token provided is invalid"},
                }
            )
        serializer = ResetUserPasswordSerializer(
            data={
                "new_password": new_password,
                "confirm_new_password": confirm_new_password,
            }
        )
        serializer.is_valid(raise_exception=True)
        user.set_password(new_password)
        user.activation_token = None
        user.save()
        return Response(
            {"message": "Password reset successful"}, status=status.HTTP_200_OK
        )
