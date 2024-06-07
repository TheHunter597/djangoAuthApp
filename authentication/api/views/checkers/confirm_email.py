from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ....models import UserModel
from ...serializers.others.user_created_kafka_serializer import (
    UserCreatedKafkaSerializer,
)
from ...kafka.user_created_producer import KafkaUserCreatedProducer
from django.http import HttpResponseRedirect
import os
from django.shortcuts import render


class ConfirmEmailAddress(APIView):
    """Confirm user email"""

    def get(self, request, token, format=None):
        """Confirm user email"""
        email, ConfirmationToken = token.split(",")
        user = UserModel.objects.filter(email=email).first()
        if user.activation_token != ConfirmationToken:
            return Response(
                {"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )
        user.activation_token = ""
        user.is_active = True
        user.account_confirmed = True
        user.retries = 0
        user.save()
        userDataForKafka = UserCreatedKafkaSerializer(user)
        userCreatedProducer = KafkaUserCreatedProducer()
        userCreatedProducer.send_message(userDataForKafka.data)

        return render(request, "authentication/account_confirmed.html")
