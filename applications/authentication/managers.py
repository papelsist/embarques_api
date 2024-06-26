from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager, models.Manager):

    def _create_user(self,username, password, is_staff, is_superuser, **extra_fields):
            user = self.model(
            username=username,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
            )
            user.set_password(password)
            print('user.password: ', user.password)
            #user.password = make_password(user.password)
            #user.save(using=self.db)
            user.save()
            return user

    def create_user(self, username, password = None, **extra_fields):
        return self._create_user(username, password, False, False, **extra_fields )

    def create_superuser(self, username, password = None, **extra_fields):
        return self._create_user(username, password, True, True, **extra_fields )