from rest_framework import views,response

class HealthView(views.APIView):
    def get(self, request, format=None):
        return response.Response({'status': 'ok'})