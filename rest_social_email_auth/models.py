# Python Modules
import logging
import datetime

# Installed Packages
import email_utils
from rest_framework import reverse

# Django Modules
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as __
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.utils import timezone

#Local Modules
from rest_social_email_auth import (
		managers, 
		app_settings,
		signals
)

# Local Variables
logger = logging.getLogger(__name__)

def generate_token():
	"""
	Get a random 64 character string


	Returns:
		str:
			A random 64 character string
	"""
	return get_random_string(length=64)


# Create your models here.
class User(AbstractUser):
	username = models.CharField(
		max_length=13,
		unique=True
	)
	email = models.EmailField(__('email address'))
	is_email_active = models.BooleanField(default=False)
	phone_regex = RegexValidator(
		regex=r'^((\+\d{1,3}(-| )?\(?\d\)?(-| )?\d{1,3})|(\(?\d{2,3}\)?))(-| )?(\d{3,4})(-| )?(\d{4})(( x| ext)\d{1,'
			  r'5}){0,1}$',
		message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
	)
	phone_number = models.CharField(
		validators=[phone_regex],
		max_length=17,
		blank=True
	)
	is_phone_active = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []
	objects = managers.CustomAccountManager()

	def __str__(self):
		return self.username


class EmailAddress(models.Model):
	"""
	A user's email address
	"""
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name=__("email")
	)
	email = models.EmailField(
		max_length=255,
		unique=True,
		verbose_name=__("email")
	)
	is_primary = models.BooleanField(
		default=False,
		help_text=__(
			"Boolean indicating if the email is the user's primary address"
		),
		verbose_name=__("is primary"),
	)
	is_verified = models.BooleanField(
		default=False,
		help_text=__(
			"Boolean indicating if the user has verified ownership of"
			"the email address"
		),
		verbose_name=__("is verified")
	)
	user = models.ForeignKey(
		get_user_model(),
		on_delete=models.CASCADE,
		related_name="email_addresses",
		related_query_name="email_address",
		verbose_name=__("user")
	)


	objects = managers.EmailAddressManager()

	class Meta(object):
		verbose_name = __("email address")
		verbose_name_plural = __("email addresses")

	def __str__(self):
		"""
		Get a string representation of the email address

		Returns:
			str:

				A text version of the email address.
		"""
		return self.email

	def send_confirmation(self):
		"""

		Send a verification email for the email address.
		"""
		confirmation = EmailConfirmation.objects.create(email=self)
		confirmation.send()

	def send_duplicate_notification(self):
		"""
		Send anotification about a duplicate sign up
		"""
		email_utils.send_email(
			from_email=settings.DEFAULT_FROM_EMAIL,
			recipient_list=[self.email],
			subject=_("Registration Attempt"),
			template_name=app_settings.PATH_TO_DUPLICATE_EMAIL_TEMPLATE,
		)

		logger.info("Sent duplicate email notification to: %s", self.email)

	def set_primary(self):
		"""
		Et this email address as the user's primary email.
		"""
		query = EmailAddress.objects.filter(is_primary=True, user=self.user)
		query = query.exclude(pk=self.pk)

		# The transaction is atomic so there is never a gap where a user has no primary email address.
		with transaction.atomic():
			query.update(is_primary=False)

			self.is_primary = True
			self.save()

		logger.info(
			"Set %s as the primary email address for %s.",
			self.email,
			self.user,
		)


class EmailConfirmation(models.Model):
	"""
	Model to store a token used to verify an email address
	"""

	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name=__("created_at")
	)
	email = models.ForeignKey(
		"rest_social_email_auth.EmailAddress",
		on_delete=models.CASCADE,
		related_name="confirmations",
		related_query_name="confirmation",
		verbose_name=__("email"),
	)
	key = models.CharField(
		default=generate_token,
		editable=False,
		max_length=255,
		verbose_name=__("confirmation key")
	)


	class Meta(object):
		verbose_name = __("email confirmation")
		verbose_name_plural = __("email confirmations")



	def confirm(self):
		"""
		Mark the intance's email as verified
		"""
		self.email.is_verified = True
		self.email.save()

		signals.email_verified.send(email=self.email, sender=self.__class__)

		logger.info("Verified email address: %s", self.email.email)


	@property
	def is_expired(self):
		"""
		Determine of the confirmation has expired


		Returns:
			bool:
			True if the confirmation has expired and False
			otherwise.
		"""
		expiration_time = self.created_at + datetime.timedelta(days=1)

		return timezone.now() > expiration_time

	def send(self):
		"""
		Send a verification email to the user
		"""
		context = {
			"verification_url": app_settings.EMAIL_VERIFICATION_URL.format(
				key=self.key
			)
		}

		email_utils.send_email(
			context=context,
			from_email=settings.EMAIL_HOST_USER,
			recipient_list=[self.email.email],
			subject=__("Please Verify Your Email Address"),
			template_name=app_settings.PATH_TO_VERIFY_EMAIL_TEMPLATE,
		)


		logger.info(
			"Sent confimration email to %s for user #%d",
			self.email.email,
			self.email.user.id,
		)