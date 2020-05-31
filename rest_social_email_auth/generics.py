# DRF Packages
from rest_framework import exceptions

class CustomException(exceptions.APIException):
	"""
	Exceptions Area


	ERROR Places
	"""
	default_detail = 'Missing Information'
	default_code = 'service_unavailable'