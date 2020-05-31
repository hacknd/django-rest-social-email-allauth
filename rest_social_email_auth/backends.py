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


# Universal List Variables of This File.
Account = get_user_model()


class AuthBackend(backends.ModelBackend):
	"""
	Authentication......starts....now
	"""
	def authenticate(self, request, username=None, password=None, token=None , **kwargs):
		if username is None:
			username = kwargs.get(Account.USERNAME_FIELD)
		try:
			"""
			 If this is an email which is blank, he or she is unable to get in with a blakn username.
			"""
			if username == '':
				msg=__('Not permitted to do this request.')
				raise CustomException(code=status.HTTP_400_BAD_REQUEST,detail=msg)
			"""
			Try to fetch the account by search the username or email field
			"""
			account = Account.objects.get(Q(username=username)|Q(email=username)|Q(phone_number=username))
			if account.check_password(password):
				return account
		except Account.DoesNotExist:
			"""
			 Run the default password hasher once to reduce the timing
			 difference between an existign and a non existing existing user
			"""
			return None

		else:
			if account.check_password(password) and self.user_can_authenticate(user):
				return	account

	def get_user(self, user_id):
		try:
			account = Account.objects.get(pk=user_id)
		except Account.DoesNotExist:
			return None
		return account if self.user_can_authenticate(account) else None 			


		
