from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ....permissions.custom_is_authenticated import CustomIsAuthenticated
from ...kafka.user_updated_producer import KafkaUserDeletedProducer
import json


class DeactivateAccount(APIView):
    permission_classes = [CustomIsAuthenticated]

    def post(self, request, format=None):
        request.user.is_active = False
        request.user.save()
        kafka_producer = KafkaUserDeletedProducer()
        kafka_producer.send_message(
            {"user_id": str(request.user.id), "data": {"is_active": False}}
        )
        response = Response(
            {"message": "Account deactivated successfully."}, status=status.HTTP_200_OK
        )
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response
