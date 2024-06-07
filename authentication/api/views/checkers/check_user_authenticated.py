from rest_framework import views, response, status
from ...serializers.main.main_user_serializer import MainUserSerializer
from ....permissions.custom_is_authenticated import (
    CustomIsAuthenticated as isAuthenticated,
)


class CheckUserAuthenticated(views.APIView):
    """check if the user is authenticated"""

    permission_classes = (isAuthenticated,)

    def get(self, request):
        """check if the user is authenticated"""
        if not request.user.account_confirmed:
            return response.Response(
                {"message": "Please confirm you account"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = MainUserSerializer(request.user)
        return response.Response(
            {"message": "User is authenticated", "user": serializer.data},
            status=status.HTTP_200_OK,
        )
