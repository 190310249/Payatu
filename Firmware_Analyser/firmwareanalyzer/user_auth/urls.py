from django.contrib import admin
from django.urls import path, include, re_path 
from django.conf import settings
from user_auth import views as User_views

urlpatterns = [
    # For Social authentication URL
    # re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('register/', User_views.UserRegistrationAPIView.as_view(), name='register'),
    path('org_register/', User_views.OrganisationRegistrationView.as_view(), name='register_organization'),
    path('login/', User_views.WebsiteAccountsUserLoginAPIView.as_view(), name='login'),
]
