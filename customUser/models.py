# Create your models here.
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    balance = models.IntegerField(default=100000)


class Transactions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return 'User: ' + self.user.username + '  Amount: ' + str(self.amount)
