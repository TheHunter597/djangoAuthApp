from rest_framework import views, response
from rest_framework.throttling import UserRateThrottle


class SustainedRateThrottle(UserRateThrottle):
    scope = "sustained"


class HealthView(views.APIView):
    throttle_classes = [SustainedRateThrottle]

    def get(self, request, format=None):
        return response.Response({"status": "ok"})
