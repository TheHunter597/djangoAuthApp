from rest_framework.views import APIView
from rest_framework.response import Response
from ....permissions.custom_is_authenticated import CustomIsAuthenticated 
from ...utils.sanitize_inputs import sanitize_inputs
from ...serializers.main.update_user_seraizer import UpdateUserSerialzer
class UpdateUser(APIView):
    """Update user data"""
    permission_classes = (CustomIsAuthenticated,)
    def put(self, request, format=None):
        user = request.user
        sanitized_inputs = sanitize_inputs(request.data)
        updated_user=UpdateUserSerialzer(user,data=sanitized_inputs,partial=True)
        if updated_user.is_valid():
            updated_user.save()
            return Response({"message":"User updated successfully","user":updated_user.data})
        return Response({"message":"User update error","errors":updated_user.errors})