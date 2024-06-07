from rest_framework import views ,status
from rest_framework.response import Response    
from rest_framework.permissions import IsAuthenticated
from ...utils.jwt.create_token import create_token

class CheckUserConfirmed(views.APIView):
    """check if the user is authenticated"""
    permission_classes = [IsAuthenticated]      
    def post(self, request):
        """check if the user is authenticated"""
        if not request.user.account_confirmed:
            return Response({"message":"User is not Confirmed"}
            ,status=status.HTTP_401_UNAUTHORIZED)
        response=Response({"message":"Account is confirmed","user":request.user.email}
            ,status=status.HTTP_200_OK)
        create_token(request.user,response)
        return response