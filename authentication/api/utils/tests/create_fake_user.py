from ....models import UserModel

def create_fake_user(client,confirmUser=False,userData={
        "email":"fdfddfdffd@gmail.com",
        "password":"12345678",
        "confirm_password":"12345678"}):
    url="/api/v1/auth/create/"
    response=client.post(url,userData)
    if confirmUser:
        confirm_created_user(userData["email"],client)
    result={
        "response":response,
        "userData":userData
    }
    return result

def confirm_created_user(email,client):
    newUser=UserModel.objects.get(email=email)
    return client.get(f"/api/v1/auth/confirm-email/{email},{newUser.activation_token}/")
