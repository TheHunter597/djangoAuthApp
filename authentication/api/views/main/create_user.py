from rest_framework import generics, status, exceptions
from ...serializers.main.create_user_serializer import CreateUserSerializer
from ...utils.jwt.create_token import create_token
from ...serializers.others.user_created_kafka_serializer import (
    UserCreatedKafkaSerializer,
)
from authentication.api.kafka.validators.validator import SchemaType
from rest_framework.response import Response
from ...utils.send_email_confirmation_token import send_email_confirmation_token
from django.db import transaction
from rest_framework.throttling import AnonRateThrottle


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    throttle_classes = [AnonRateThrottle]
    serializer_class = CreateUserSerializer

    def post(self, request):
        """Create a new user with encrypted password and return it"""
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    new_user = serializer.save()
                    userData = UserCreatedKafkaSerializer(new_user).data
                    SchemaType.validate(userData, "userCreated")
                    send_email_confirmation_token(
                        new_user.email, new_user.activation_token
                    )
                    response = Response(
                        {
                            "message": "Confirmation link has been sent to your email",
                            "user": userData,
                        },
                        status=status.HTTP_201_CREATED,
                    )
                    create_token(new_user, response)
                    return response
            except Exception as e:
                raise exceptions.ValidationError(
                    {"message": "User creation error", "errors": e.detail}
                )
        raise exceptions.ValidationError(
            {"message": "User creation error", "errors": serializer.errors}
        )
