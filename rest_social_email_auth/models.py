# Django Modules
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as __

#Local Modules
from rest_social_email_auth import managers

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
