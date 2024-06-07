from rest_framework.test import APITestCase, APIClient
from .api.utils.tests.create_fake_user import create_fake_user
from unittest.mock import patch
from django.contrib.auth import get_user_model


def mock(firs):
    return None


def mock_send_message(self, message):
    return None


@patch(
    "authentication.api.kafka.user_created_producer.KafkaUserCreatedProducer.__init__",
    mock,
)
@patch(
    "authentication.api.kafka.user_created_producer.KafkaUserCreatedProducer.send_message",
    mock_send_message,
)
class UserTests(APITestCase):
    userModel = get_user_model()
    right_params = {
        "email": "fdfddfdffd@gmail.com",
        "password": "12345678",
        "confirm_password": "12345678",
    }
    url = "/api/v1/auth/create/"

    def test_create_user_with_wrong_params(self):
        """Test creating a new user"""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "User creation error")
        self.assertEqual(response.data["errors"]["email"][0], "This field is required.")
        self.assertEqual(
            response.data["errors"]["password"][0], "This field is required."
        )
        self.assertEqual(
            response.data["errors"]["confirm_password"][0], "This field is required."
        )
        response = self.client.post(self.url, {"email": "dfddfdffd@gmail.com"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "User creation error")
        self.assertEqual(
            response.data["errors"]["password"][0], "This field is required."
        )

    def test_create_user_with_wrong_email(self):
        """Test creating a new user"""
        response = self.client.post(
            self.url, {"email": "dfddfdffd", "password": "12345678"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "User creation error")
        self.assertEqual(
            response.data["errors"]["email"][0], "Enter a valid email address."
        )

    def test_create_user_with_wrong_password(self):
        """Test creating a new user"""
        response = self.client.post(
            self.url,
            {
                "email": "dfddfdffd@gmail.com",
                "password": "1234",
                "confirm_password": "1234",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "User creation error")
        self.assertEqual(
            response.data["errors"]["password"][0],
            "Ensure this field has at least 8 characters.",
        )

    def test_create_user_with_passwords_not_matching(self):
        """Test creating a new user"""
        response = self.client.post(
            self.url,
            {
                "email": "dfddfdffd@gmail.com",
                "password": "123hgghg4",
                "confirm_password": "123hggdfgfd",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "User creation error")
        self.assertEqual(response.data["errors"]["password"][0], "passwords must match")
        self.assertEqual(
            response.data["errors"]["confirm_password"][0], "passwords must match"
        )

    def test_create_user_with_right_params(self):
        """Test creating a new user"""
        response = create_fake_user(self.client)["response"]
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user"]["email"], self.right_params["email"])
        self.assertEqual(
            response.data["message"], "Confirmation link has been sent to your email"
        )

    def test_if_email_is_duplicate(self):
        """Test creating a new user"""
        firstUser = create_fake_user(self.client)["response"]
        self.assertEqual(firstUser.status_code, 201)
        secondUser = create_fake_user(self.client)["response"]
        self.assertEqual(secondUser.status_code, 400)
        self.assertEqual(secondUser.data["message"], "User creation error")
        self.assertEqual(
            secondUser.data["errors"]["email"][0], "This email already exists."
        )


@patch(
    "authentication.api.kafka.user_created_producer.KafkaUserCreatedProducer.__init__",
    mock,
)
@patch(
    "authentication.api.kafka.user_created_producer.KafkaUserCreatedProducer.send_message",
    mock_send_message,
)
class UserLoginTests(APITestCase):
    userModel = get_user_model()
    url = "/api/v1/auth/login/"

    def test_login_with_withour_params(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "User not found")
        self.assertEqual(response.data["errors"]["email"][0], "Email wasnt provided")
        self.assertEqual(
            response.data["errors"]["password"][0], "Password wasnt provided"
        )

    def test_login_with_wrong_email(self):
        response = self.client.post(
            self.url, {"email": "dfddfdffd", "password": "12345678"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "User not found")
        self.assertEqual(
            response.data["errors"]["email"][0], "Email or password is wrong"
        )
        self.assertEqual(
            response.data["errors"]["password"][0], "Email or password is wrong"
        )

    def test_login_with_wrong_password(self):
        userData = create_fake_user(self.client)["userData"]
        response = self.client.post(
            self.url, {"email": userData["email"], "password": "fgfgfgfg"}
        )
        self.assertEqual(response.data["message"], "User not found")
        self.assertEqual(
            response.data["errors"]["email"][0], "Email or password is wrong"
        )
        self.assertEqual(
            response.data["errors"]["password"][0], "Email or password is wrong"
        )

    def test_login_with_right_params(self):
        userData = create_fake_user(self.client, True)["userData"]
        response = self.client.post(
            self.url, {"email": userData["email"], "password": userData["password"]}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user"]["email"], userData["email"])
        self.assertEqual(response.data["message"], "User logged in successfully")
        self.assertTrue(response.cookies["refresh"])
        self.assertTrue(response.cookies["access"])


@patch(
    "authentication.api.kafka.user_created_producer.KafkaUserCreatedProducer.__init__",
    mock,
)
@patch(
    "authentication.api.kafka.user_created_producer.KafkaUserCreatedProducer.send_message",
    mock_send_message,
)
class TestUserUpdate(APITestCase):
    userModel = get_user_model()

    def __init__(self, methodName: str = "runTest") -> None:
        client = APIClient()
        self.url = "/api/v1/auth/update/"
        self.client = client
        super().__init__(methodName)

    def test_update_user_without_being_authenticated(self):
        response = self.client.put(self.url, {})
        self.assertEqual(response.status_code, 401)
        print({"lsjdfsdf": response.data})
        self.assertEqual(response.data["detail"], "Please login to do this action.")

    def test_update_user_with_wrong_params(self):
        response = create_fake_user(self.client, True)["response"]
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response.cookies.get("access").value
        )
        result = self.client.put(
            self.url,
            {"first_name": "mangomanmangomanmangomanmangomanmangomanmangomanmangoman"},
        )
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data["message"], "User update error")
        self.assertEqual(
            result.data["errors"]["first_name"][0],
            "Ensure this field has no more than 30 characters.",
        )

    def test_update_user_with_right_params(self):
        response = create_fake_user(self.client, True)["response"]
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response.cookies.get("access").value
        )
        response = self.client.put(self.url, {"first_name": "mangoman"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "User updated successfully")
        self.assertEqual(response.data["user"]["first_name"], "mangoman")


@patch(
    "authentication.api.kafka.user_created_producer.KafkaUserCreatedProducer.__init__",
    mock,
)
@patch(
    "authentication.api.kafka.user_created_producer.KafkaUserCreatedProducer.send_message",
    mock_send_message,
)
class ChangeUserPassword(APITestCase):
    pass

    def __init__(self, methodName: str = "runTest") -> None:
        client = APIClient()
        self.url = "/api/v1/auth/change-password/"
        client = client
        super().__init__(methodName)

    def test_change_password_without_being_authenticated(self):
        response = self.client.patch(self.url, {})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "Please login to do this action.")

    def test_change_password_with_without_params(self):
        response = create_fake_user(self.client, True)["response"]
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response.cookies.get("access").value
        )
        result = self.client.patch(self.url, {})
        self.assertEqual(result.status_code, 400)
        self.assertEqual(
            result.data["message"], "Error happened while changing password"
        )
        self.assertEqual(
            result.data["errors"]["old_password"][0], "This field is required."
        )
        self.assertEqual(
            result.data["errors"]["new_password"][0], "This field is required."
        )
        self.assertEqual(
            result.data["errors"]["confirm_new_password"][0], "This field is required."
        )

    def test_change_password_with_wrong_old_password(self):
        data = create_fake_user(self.client, True)
        response = data["response"]
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response.cookies.get("access").value
        )
        result = self.client.patch(
            self.url,
            {
                "old_password": "testdddd",
                "new_password": "12345678",
                "confirm_new_password": "12345678",
            },
        )
        self.assertEqual(result.status_code, 400)
        self.assertEqual(
            result.data["message"], "Error happened while changing password"
        )
        self.assertEqual(
            result.data["errors"]["old_password"][0], "Old password is wrong"
        )

    def test_change_password_with_news_not_the_same(self):
        data = create_fake_user(self.client, True)
        response = data["response"]
        userData = data["userData"]
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response.cookies.get("access").value
        )
        result = self.client.patch(
            self.url,
            {
                "old_password": userData["password"],
                "new_password": "12345678",
                "confirm_new_password": "123456789",
            },
        )
        self.assertEqual(result.status_code, 400)
        self.assertEqual(
            result.data["message"], "Error happened while changing password"
        )
        self.assertEqual(
            result.data["errors"]["new_password"][0],
            "New password and confirm new password must match",
        )
        self.assertEqual(
            result.data["errors"]["confirm_new_password"][0],
            "New password and confirm new password must match",
        )

    def test_change_password_with_wrong_new_password_validation(self):
        data = create_fake_user(self.client, True)
        response = data["response"]
        userData = data["userData"]
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response.cookies.get("access").value
        )
        result = self.client.patch(
            self.url,
            {
                "old_password": userData["password"],
                "new_password": "1234",
                "confirm_new_password": "1234",
            },
        )
        self.assertEqual(result.status_code, 400)
        self.assertEqual(
            result.data["message"], "Error happened while changing password"
        )
        self.assertEqual(
            result.data["errors"]["new_password"][0],
            "Password must be at least 8 characters long",
        )

    def test_change_password_with_right_params(self):
        data = create_fake_user(self.client, True)
        response = data["response"]
        userData = data["userData"]
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response.cookies.get("access").value
        )
        result = self.client.patch(
            self.url,
            {
                "old_password": userData["password"],
                "new_password": "12345678",
                "confirm_new_password": "12345678",
            },
        )
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data["message"], "Password changed successfully")
