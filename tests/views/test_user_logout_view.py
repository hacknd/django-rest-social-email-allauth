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

class UserTokenLogoutTest(APITestCase):
	def token_verification(self, auth_token):
		token = auth_token.split("Token ")[1]
		return token[:settings.CONSTANTS.TOKEN_KEY_LENGTH]

	def setUp(self):
		"""
		Originally creating a user from scratch to add up to users at the same time
		:return:
		"""
		self.test_user = get_user_model().objects.create_user(
			username="testuser",
			email="test@example.com",
			password="testpassword",
			phone_number="+254715943570"
		)
		self.test_user.save()
		self.create_url = url

	def test_authenticated_account_with_token_recognition_decides_to_logout_for_a_specific_device(self):
		"""
		Ensuring the user in the system has token Authenticatian naa mean and log out once
		"""
		self.assertEqual(AuthToken.objects.count(), 0)
		# account = Account.objects.latest('id')

		data = {
			'username': 'test@example.com',
			'password': 'testpassword',
		}

		response = self.client.post(self.create_url, data, format='json')
		self.assertEqual(AuthToken.objects.count(), 1)
		self.assertEqual(self.token_verification(response['Authorization']),
						 AuthToken.objects.latest('user_id').token_key)
		self.client.post(self.create_url, data, format='json')
		self.assertTrue(all(e.token_key for e in AuthToken.objects.all()))
		url = reverse('rest-social-email-auth:user-logout')
		self.client.credentials(HTTP_AUTHORIZATION=response['Authorization'])
		self.client.post(url, {}, format='json')
		self.assertEqual(AuthToken.objects.count(), 1, 'other tokens should remain after logout')

	def test_authenticated_account_with_token_recognition_decides_to_logout_for_all_devices(self):
		"""
		Ensuring the user in the system has token Authenticatian naa mean and log out once
		"""
		self.assertEqual(AuthToken.objects.count(), 0)
		# account = Account.objects.latest('id')

		data = {
			'username': 'test@example.com',
			'password': 'testpassword',
		}

		response = self.client.post(self.create_url, data, format='json')
		self.assertEqual(AuthToken.objects.count(), 1)
		self.assertEqual(self.token_verification(response['Authorization']),
						 AuthToken.objects.latest('user_id').token_key)
		self.client.post(self.create_url, data, format='json')
		self.assertTrue(all(e.token_key for e in AuthToken.objects.all()))
		url = reverse('rest-social-email-auth:user-logout-all')
		self.client.credentials(HTTP_AUTHORIZATION=response['Authorization'])
		self.client.post(url, {}, format='json')
		self.assertEqual(AuthToken.objects.count(), 0,
						 'everyone instance of the user does not get the authentication access')
