from django.contrib import admin

from customUser.models import CustomUser, Transactions

admin.site.register(CustomUser)
admin.site.register(Transactions)
