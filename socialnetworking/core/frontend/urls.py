
from django.urls import path

from .views import *

urlpatterns = [
    path('', home),
    path('sign-up/', sign_up),
    path('login/', sign_in),
    path('logout/', logout_view),
    path('home/', home),
]



