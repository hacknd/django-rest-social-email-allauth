# Django Packages
from django.urls import path

# Local Packages
from rest_social_email_auth import views

app_name = "rest-social-email-auth"


urlpatterns = [
	path(
		'register/',
		views.UserCreateView.as_view(),
		name='user-create'
	),
	path(
		'login/',
		views.UserLoginView.as_view(),
		name='user-login'
	),
	path(
		'logout/',
		views.UserLogoutView.as_view(),
		name='account-logout'
	),
	path(
		'logout-all/',
		views.UserLogoutAllView.as_view(),
		name='account-logout-all'
	),
]