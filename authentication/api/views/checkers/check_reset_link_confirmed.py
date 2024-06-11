from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ...utils.jwt.create_token import create_token
from ....models import UserModel
from django.http import HttpResponseRedirect


class CheckResetLinkConfirmed(views.APIView):

    def post(self, request):
        """Reset user password"""
        email = request.POST.get("email")
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response(
                {"message": "User not found", "errors": {"email": ["Email not found"]}},
                status=status.HTTP_404_NOT_FOUND,
            )
        if len(user.activation_token) > 1:
            return Response(
                {"message": "Please check your email for the reset link"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        import os

        base_url = os.getenv("BASE_URL")
        return HttpResponseRedirect(
            redirect_to=f"{base_url}/reset-password/{create_token(user)}/"
        )
