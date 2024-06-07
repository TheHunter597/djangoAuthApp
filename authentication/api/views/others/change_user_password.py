from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ....permissions.custom_is_authenticated import (
    CustomIsAuthenticated as IsAuthenticated,
)

from ...serializers.others.update_password_serializer import UpdateUserPassword
from rest_framework.serializers import ValidationError


class ChangeUserPassword(APIView):
    """Change user password"""

    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        """Change user password"""
        user = request.user
        serializer = UpdateUserPassword(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password changed successfully"}, status=status.HTTP_200_OK
            )
        raise ValidationError(
            {
                "message": "Error happened while changing password",
                "errors": serializer.errors,
            }
        )
