from django import dispatch


user_registered = dispatch.Signal(providing_args=["user"])

email_verified = dispatch.Signal(providing_args=["email"])