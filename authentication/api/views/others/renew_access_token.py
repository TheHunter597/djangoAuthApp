from rest_framework import views, permissions, response, status
from rest_framework_simplejwt.tokens import RefreshToken


class RenewAccessToken(views.APIView):
    """Renew access token"""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Renew access token"""
        refresh_token = request.COOKIES.get("refresh")
        if not refresh_token:
            return response.Response(
                {"message": "No refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            refresh_token = RefreshToken(refresh_token)
            refresh_token.verify()
            access_token = str(refresh_token.access_token)
            renewdResponse = response.Response({"message": "Access token renewed"})
            renewdResponse.set_cookie(key="access", value=access_token)
            return renewdResponse
        except Exception as e:
            print(e)
            return response.Response(
                {"message": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )
