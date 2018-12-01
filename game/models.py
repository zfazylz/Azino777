from django.conf import settings
from django.db import models

from customUser.models import CustomUser


class BetRoll(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    betValue = models.IntegerField(default=0)
    winLoseValue = models.IntegerField(default=0, null=True)
    combination = models.CharField(default=None, max_length=6, null=True)

    def __str__(self):
        return 'User: ' + self.user.username + '  Bet: ' + str(self.betValue) + '  Result: ' + str(
            self.winLoseValue) + '  Combo: ' + self.combination
