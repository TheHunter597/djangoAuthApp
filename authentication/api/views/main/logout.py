from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ....permissions.custom_is_authenticated import CustomIsAuthenticated 

class Logout(APIView):
    permission_classes= [CustomIsAuthenticated]
    def get(self, request, format=None):
        response=Response(status=status.HTTP_200_OK)
        response.delete_cookie("refresh")
        response.delete_cookie("access")
        return response