# DRF Packages
from rest_framework import exceptions
from rest_framework import generics, status
from rest_framework.response import Response

class CustomException(exceptions.APIException):
	"""
	Exceptions Area


	ERROR Places
	"""
	default_detail = 'Missing Information'
	default_code = 'service_unavailable'


class SerializerSaveView(generics.GenericAPIView):
	"""
	Generic view from saving a serializer and returning the results.
	"""

	def post(self, request):
		"""
		Save the provided data using the class' serializer.

		Args:
			request:
				The request being made.


		Returns:
			An ``APIResponse`` instance. If the request was successful
			the response will have a 200 status code and contain the
			serializer's data. Otherwise a 400 statu code and the request's
			errors will be returned.
		"""
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			serializer.save()


			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	# We reset the docstring becuase it's used to generat DRF's docs,
	# and documentation on the ' post' method has a higher specificity
	# than a class-level docstring.
	post.__doc__ = ""