# DRF Packages
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# Installed Packages
from knox.models import AuthToken
from knox import settings

# Django Packages
from django.contrib.auth import get_user_model

url = reverse("rest-social-email-auth:user-login")

# response = api_client.post(url, data)


def test_authenticate_account_with_username(api_client, user_factory):
    """
	Ensuring the user is in the system and does the spot yaamean I was listening to reggae writing affi man
	:return:

	"""
    user_account = user_factory()

    data = {"username": user_account.username, "password": "password"}
    response = api_client.post(url, data)
    assert response.data["user"]["username"] == data["username"]
    assert user_account.check_password(data["password"])


def test_authenticate_account_with_email(api_client, user_factory):
    """
	Ensuring the user is in the system and does the activatian with email yaa mean is a plan
	:return:
	"""
    user_account = user_factory()

    data = {"username": user_account.email, "password": "password"}
    response = api_client.post(url, data)
    assert response.data["user"]["email"] == data["username"]
    assert user_account.check_password(data["password"])


def test_authenticate_account_with_phone_number(api_client, user_factory):
    """
	Ensuring the user is in the system and does the activatian with email yaa mean is a plan
	:return:
	"""
    user_account = user_factory()

    data = {"username": user_account.phone_number, "password": "password"}
    response = api_client.post(url, data)
    print(response.data)
    assert response.data["user"]["phone_number"] == data["username"]
    assert user_account.check_password(data["password"])


class AccountTokenLoginTest(APITestCase):
    def token_verification(self, auth_token):
        token = auth_token.split("Token ")[1]
        return token[: settings.CONSTANTS.TOKEN_KEY_LENGTH]

    def setUp(self):
        """
		Originally creating a user from scratch to add up to users at the same time
		:return:
		"""
        self.test_user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            phone_number="+254715943570",
        )
        self.test_user.save()
        self.create_url = url

    def test_authenticate_account_with_token_recognition(self):
        """
		Ensuring the user in the system has token Authenticatian naa mean
		"""
        self.assertEqual(AuthToken.objects.count(), 0)
        # account = Account.objects.latest('id')

        data = {
            "username": "test@example.com",
            "password": "testpassword",
        }

        response = self.client.post(self.create_url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=response["Authorization"])
        self.assertEqual(AuthToken.objects.count(), 1)
        self.assertEqual(
            self.token_verification(response["Authorization"]),
            AuthToken.objects.latest("user_id").token_key,
        )
        self.assertEqual(1, 1)
        self.assertTrue(all(e.token_key for e in AuthToken.objects.all()))
