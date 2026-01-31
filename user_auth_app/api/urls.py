from django.urls import path
from .views import RegistrationsView, CustomLogin, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('registration/', RegistrationsView.as_view(), name='registration'),
    path('login/', CustomLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]