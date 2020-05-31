#Django packages
from django.utils.translation import gettext_lazy as __
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
#Rest Framework Packages
from rest_framework import test, reverse
#Local packages installed
import httpretty
import json
import requests
import unittest

EPIC_JSON={
	"token": "487793df5d9fd76966a8ff1d3915e8035482597944a230355d44e0a92a52edee",
	"expiry": "2019-05-29T20:18:48.768478Z",
	"user": {
		"id": 2,
		"token": "487793df5d9fd76966a8ff1d3915e8035482597944a230355d44e0a92a52edee",
		"first_name": "",
		"last_name": "",
		"username": "_ber.ni.e_",
		"email": "benkaranja43@gmail.com",
		"is_email_active": False,
		"phone_number": "",
		"is_phone_active": False
	}
}
class AccountSocialAccountTest(test.APITestCase):
	def setUp(self):
		'''
		Setting up the new site for the new default application
		'''
		httpretty.enable()
		
	def _domain_information_pull_with_json(self, provider):
		return json.dumps(
			{
			"code":"oofgawd",
			"redirect_uri":(('http://{}{}').format(Site.objects.get_current().domain, reverse.reverse('rest-social-email-auth:user-social-login', args=(provider,)))).replace('example.com', 'localhost:8000'),
			"provider":provider
			}
			)

	def test_social_account_with_no_valid_provider(self):
		'''
		Testing the instance of a foreign backend
		'''
		provider='facebook'
		resp = self.client.get(reverse.reverse('rest-social-email-auth:user-social-login', args=(provider,)))
		self.assertEqual(resp.status_code, 500)
		self.assertEqual(resp.data['detail'], __('Missing Backend'))
	
	def test_social_account_for_discord(self):
		'''
		Testing instance for discord application
		'''	
		self.provider='discord'
		resp = self.client.get(reverse.reverse('rest-social-email-auth:user-social-login', args=(self.provider,)))
		self.assertEqual(resp.status_code, 302)	
		httpretty.register_uri(
			httpretty.GET,
			resp.url,
			body=self._domain_information_pull_with_json(self.provider),
			status=200
			)
		response=requests.get(resp.url)
		httpretty.register_uri(
			httpretty.POST,
			response.json()['redirect_uri'],
			body=json.dumps(EPIC_JSON),
			status=201,
			content_type='text/json'
			)	
		custom_resp=requests.post(response.json()['redirect_uri'], response.json())
		self.assertEqual(custom_resp.status_code, 201)
		self.assertEqual(custom_resp.json()['token'],custom_resp.json()['user']['token'] )	
	def tearDown(self):
		httpretty.disable()	