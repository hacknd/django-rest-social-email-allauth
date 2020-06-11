# Django Packages
from django.contrib.auth import (
		get_user_model, 
		backends
)
from django.db.models import Q
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as __

# DRF PAckages
from rest_framework import (
		authentication,
		exceptions,
		status
)
from rest_framework.response import Response
from rest_framework import exceptions

# Local Packages
from rest_social_email_auth.generics import CustomException
from rest_social_email_auth import models

# Universal List Variables of This File.
Account = get_user_model()


class AuthBackend(backends.ModelBackend):
	"""
	Authentication......starts..now
	"""

	def authenticate(self, request, username=None, email=None, password=None, token=None, **kwargs):
		"""

		:param token:
		:param password:
		:param username:
		:param request:
		:type kwargs: object
		"""
		
		username = email or username

		try:
			"""
			If this is an email which is blank, he or she is unable to get in with a blank username
			"""
			if username == None:
				msg = __('Not permitted to do this request.')
				raise GamEngineException(code=status.HTTP_400_BAD_REQUEST, detail=msg)
			"""
			Try to fetch the account by search the username or email field
			"""
			account = Account.objects.get(Q(username=username) | Q(email=username) | Q(phone_number=username))
			if account.check_password(password):
				return account
		except Account.DoesNotExist:
			"""
			Run the default password hashes once to reduce the timing
			difference between an existing and a non existing user
			"""
			return None
		

	def get_user(self, user_id):
		try:
			account = get_user_model().objects.get(id=user_id)
		except get_user_model().DoesNotExist:
			return None
		return account if self.user_can_authenticate(account) else None

class VerifiedEmailBackend(AuthBackend):
	"""
	Authentication backend that only allows for the use of verified email addresses.
	"""
	
	def authenticate(self, request, email=None, password=None, username=None):
		"""
		Attempt to authenticate a set of credentials.

		Args:
			request:
				The request associated with the authentication attempt.
			email:
				The user's email address.
			password:
				The user's password.
			username:
				An alias for the ``email`` field. This is provided for 
				compatibilty with Django's built in authentication views.

		Returns:
			The user associated with the provided credentials if they are valid.
			Returns ``None`` otherwise.
		"""
		email = email or username

		try:
			email_instance = models.EmailAddress.objects.get(
				is_verified=True, email=email
			)
		except models.EmailAddress.DoesNotExist:
			return None

		user = email_instance.user

		if user.check_password(password):
			return user

		return None