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
        serializer = ResetUserPasswordSerializer(
            data={
                "new_password": new_password,
                "confirm_new_password": confirm_new_password,
                "email": email,
                "confirmation_token": confirmation_token,
            }
        )
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(new_password)
            user.activation_token = None
            user.save()
            return Response(
                {"message": "Password changed successfully"}, status=status.HTTP_200_OK
            )
        else:
            raise serializers.ValidationError(
                {
                    "message": "Error happened while changing password",
                    "errors": serializer.errors,
                }
            )
