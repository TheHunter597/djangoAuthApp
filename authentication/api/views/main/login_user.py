from rest_framework import views, exceptions, status
from rest_framework.response import Response
from ....models import UserModel
from ...serializers.main.login_user_serializer import BasicUserDataSerializer
from ...utils.jwt.create_token import create_token


class LoginUser(views.APIView):
    """login serializer for the user object"""

    serializer_class = BasicUserDataSerializer

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        if not email or not password:
            raise exceptions.ValidationError(
                {
                    "message": "User not found",
                    "errors": {
                        "email": ["Email wasnt provided"],
                        "password": ["Password wasnt provided"],
                    },
                }
            )

        try:
            user = UserModel.objects.get(email=request.data["email"])
        except UserModel.DoesNotExist:
            raise exceptions.ValidationError(
                {
                    "message": "User not found",
                    "errors": {
                        "email": ["Email or password is wrong"],
                        "password": ["Email or password is wrong"],
                    },
                }
            )
        if not user.check_password(request.data["password"]):
            raise exceptions.ValidationError(
                {
                    "message": "User not found",
                    "errors": {
                        "email": ["Email or password is wrong"],
                        "password": ["Email or password is wrong"],
                    },
                }
            )
        if user.account_confirmed == False:
            raise exceptions.ValidationError(
                {
                    "message": "User not found",
                    "errors": {
                        "email": ["Email not confirmed"],
                        "password": ["Email not confirmed"],
                    },
                }
            )
        if user.is_active == False:
            raise exceptions.ValidationError(
                {
                    "message": "User not found",
                    "errors": {
                        "email": ["Account deactivated"],
                        "password": ["Account deactivated"],
                    },
                }
            )
        serializer = BasicUserDataSerializer(user)
        response = Response(
            {"message": "User logged in successfully", "user": serializer.data},
            status=status.HTTP_200_OK,
        )
        create_token(serializer.instance, response)
        return response
