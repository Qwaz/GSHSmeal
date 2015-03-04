from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class User(PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    last_login = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ()

    def is_authenticated(self):
        return True

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin
