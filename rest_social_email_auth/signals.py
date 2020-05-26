from django import dispatch


user_registered = dispatch.Signal(providing_args=["user"])