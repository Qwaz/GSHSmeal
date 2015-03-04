from django.contrib import messages

from gshs_auth.login_api import login
from gshs_auth.models import User


class UserBackend(object):
    def authenticate(self, username, rsa_id, rsa_password, jsession_id, request=None):
        login_result = login(rsa_id, rsa_password, jsession_id)

        if isinstance(login_result, str):
            if request:
                messages.error(request, login_result)
            return None
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
                user.save()
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
