from django.urls import path

from .views import *

urlpatterns = [
    path('game/', gamePageView, name='game'),
    path('', homePageView, name='home'),
    path('fillCash/', fillCashView, name='fillCash'),
    path('withdrawCash/', withdrawCashView, name='withdrawCash'),

]
