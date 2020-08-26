from django.urls import path
#from django.views.generic.base import TemplateView
from .views import *


urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view()),
]