from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.backends import TokenBackend
from django.conf import settings
import os
import time


class CustomIsAuthenticated(BasePermission):
    """Custom permission class to allow only authenticated users."""

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.is_active:
            self.message = "You are authenticated"
            return True
        else:
            self.message = {"message": "Please login to do this action."}
            raise AuthenticationFailed(self.message)
