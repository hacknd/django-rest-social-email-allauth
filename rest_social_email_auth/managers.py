# Django Packages
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as __
from django.db import models, transaction
from django.utils import timezone
from rest_social_email_auth import app_settings as settings


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
        if extra_fields.get("is_superuser"):
            if email == "":
                pass
            account = self.model(username=username, **extra_fields)
            account.set_password(extra_fields.get("password"))
            account.save()
            return account
        if not email:
            raise ValueError(__("The Email must be set"))

        email = self.normalize_email(email)
        account = self.model(username=username, email=email, **extra_fields)
        account.set_password(extra_fields.get("password"))

        account.save()

        return account

    def create_superuser(self, username, password, email=None, **extra_fields):
        """
		Create and save a superuser account with username and password
		"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(__("superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(__("superuser must have is_superuser=True"))
        super_user_account = self.create_user(
            username=username, email=email, password=password, **extra_fields
        )
        super_user_account.save()

        return super_user_account


class EmailAddressManager(models.Manager):
    """
	Manager for email address intances
	"""

    def create(self, *args, **kwargs):
        """
		Create a new email address
		"""
        is_primary = kwargs.pop("is_primary", False)

        with transaction.atomic():
            email = super(EmailAddressManager, self).create(*args, **kwargs)

            if is_primary:
                email.set_primary()

        return email


class ValidPasswordResetTokenManager(models.Manager):
    """
	Manager for getting only valid password reset tokens.


	Valid tokens are those that have not yet expired
	"""

    def get_queryset(self):
        """
		Return all unexpired password reset tokens.
		"""
        oldest = timezone.now() - settings.PASSWORD_RESET_EXPIRATION
        queryset = super(ValidPasswordResetTokenManager, self).get_queryset()

        return queryset.filter(created_at__gt=oldest)
