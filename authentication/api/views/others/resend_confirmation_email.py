from rest_framework import generics, status, exceptions
from rest_framework.response import Response
from ....permissions.custom_is_authenticated import CustomIsAuthenticated
from ...utils.send_email_confirmation_token import send_email_confirmation_token
from django.db.models import F


class ResendConfirmationEmail(generics.CreateAPIView):
    """Create a new user in the system"""

    permission_classes = [CustomIsAuthenticated]

    def post(self, request):
        """Create a new user with encrypted password and return it"""

        if request.user.account_confirmed:
            raise exceptions.ValidationError({"message": "User already confirmed"})
        user = request.user
        user.retries = user.retries + 1
        if user.retries >= 3:
            raise exceptions.ValidationError(
                {"message": "You have exceeded the number of retries"}
            )
        user.save()
        send_email_confirmation_token(request.user.email, request.user.activation_token)
        response = Response(
            {
                "message": "Confirmation link has been sent to your email",
                "user": request.user.email,
            },
            status=status.HTTP_201_CREATED,
        )
        return response
