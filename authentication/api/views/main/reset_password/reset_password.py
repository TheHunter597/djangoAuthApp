from rest_framework.views import APIView
from rest_framework import views, exceptions, status
from .....models import UserModel
from authentication.api.utils.create_confirmation_token import create_confirmation_token
from ....utils.send_password_reset_token import send_password_reset_token
from django.db.models import F
from rest_framework.throttling import AnonRateThrottle


class ResetUserPassword(APIView):
    """Reset user password"""

    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        email = request.data["email"]
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise exceptions.ValidationError(
                {
                    "message": "User not found",
                    "errors": {
                        "email": ["Email not found"],
                    },
                }
            )
        user.retires = user.retries + 1
        if user.retries >= 3:
            raise exceptions.ValidationError(
                {
                    "message": "You have exceeded the number of retries",
                }
            )
        user.activation_token = create_confirmation_token()
        send_password_reset_token(user.email, user.activation_token)
        user.retires = 0
        user.save()

        return views.Response(
            {"message": "Password reset link has been sent to your email"},
            status=status.HTTP_200_OK,
        )
