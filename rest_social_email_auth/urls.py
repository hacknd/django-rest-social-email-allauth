# Django Packages
from django.urls import path

# Local Packages
from rest_social_email_auth import views

app_name = "rest-social-email-auth"


urlpatterns = [
	path(
		'register/',
		views.AccountCreateView.as_view(),
		name='account-create'
	),
	
]