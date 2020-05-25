# Django Packages
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as __


class CustomAccountManager(BaseUserManager):
	"""
	Custom Account Model Manager used to show it suppose to do 
	during account creation and super creation
	"""
	def create_user(self, username, email, **extra_fields):
		"""
		Create and save individual account with given email and password

		Args:
			self - class instance.
			username - username input from the post request.
			email - email input from the post request.
			**extra_fields - added variables placed during the creation of an account.
		
		Returns:
			Saved Account.
		"""
		if extra_fields.get('is_superuser'):
			if email == '':
				pass
			account = self.model(username=username, **extra_fields)
			account.set_password(extra_fields.get('password'))
			account.save()
			return account
		if not email:
			raise ValueError(__('The Email must be set'))

		email = self.normalize_email(email)
		account = self.model(username=username, email=email, **extra_fields)
		account.set_password(extra_fields.get('password'))

		account.save()

		return account

	def create_superuser(self, username, password, email=None, **extra_fields):
		"""
		Create and save a superuser account with username and password
		"""
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError(__('superuser must have is_staff=True'))
		if extra_fields.get('is_superuser') is not True:
			raise ValueError(__('superuser must have is_superuser=True'))
		super_user_account = self.create_user(username=username, email=email, password=password, **extra_fields)
		super_user_account.save()

		return super_user_account
