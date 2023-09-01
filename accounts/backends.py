from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            # Check if the entered identifier is a username
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            # If not a username, then try with email
            try:
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password):
            return user

        return None
