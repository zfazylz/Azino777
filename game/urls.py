from django.urls import path

from .views import *

urlpatterns = [
    path('game/', gamePageView, name='game'),
    path('', homePageView, name='home'),
    # path('signup/', views.SignUp.as_view(), name='signup'),
    path('fillCash/', fillCashView, name='fillCash'),
    path('withdrawCash/', withdrawCashView, name='withdrawCash'),

]
