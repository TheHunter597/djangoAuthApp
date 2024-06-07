from rest_framework_simplejwt.backends import TokenBackend
import os
import time
from rest_framework_simplejwt.tokens import RefreshToken


class TokensRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        refresh_token = request.COOKIES.get("refresh")
        if not refresh_token:
            return response
        try:
            token = request.headers["Authorization"].split(" ")[1]
            token_backend = TokenBackend(
                algorithm="HS256",
                signing_key=(
                    os.getenv("SECRET_KEY")
                    if os.getenv("ENV") == "PRODUCTION"
                    else "test-secret-key"
                ),
            )

            try:
                decoded_token = token_backend.decode(token)
            except Exception as e:
                decoded_refresh = token_backend.decode(refresh_token)
                if decoded_refresh:
                    refresh_token = RefreshToken(refresh_token)
                    refresh_token.verify()
                    access_token = str(refresh_token.access_token)
                    response.set_cookie(key="access", value=access_token)
                    return response
            current_time = int(time.time())
            expiration_time = decoded_token["exp"]

            if expiration_time - current_time <= 600:
                refresh_token = RefreshToken(refresh_token)
                refresh_token.verify()
                access_token = str(refresh_token.access_token)
                response.set_cookie(key="access", value=access_token)
                return response
            else:
                return response
        except Exception as e:
            return response
