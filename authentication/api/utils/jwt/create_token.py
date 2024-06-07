from rest_framework_simplejwt.tokens import RefreshToken

def create_token(data,response):
    token = RefreshToken.for_user(data)
    token["first_name"] = data.first_name
    token["last_name"] = data.last_name
    token["email"] = data.email
    token["avatar"] = data.avatar
    token["is_active"] = data.is_active
    token["is_superuser"] = data.is_superuser
    token["is_staff"] = data.is_staff
    token["account_confirmed"] = data.account_confirmed
    response.set_cookie("refresh", str(token), httponly=True)
    response.set_cookie("access", str(token.access_token))