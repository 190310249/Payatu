from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserModel, OrganisationModel
from django.contrib.auth import get_user_model
from rest_framework import generics, views
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# from account import 


# Create your views here.
    
def otp(self):
    send_mail(
        'Subject here',
        'Here is the message.',
        'noreply@xyz.com',
        ['pratikmajhi123@gmail.com'],
        fail_silently=False,
    )
    return True

class UserRegistrationAPIView(generics.GenericAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        try:
            data = request.data
            queryset = self.queryset.all()
            if queryset.filter(email=data["email"]).exists():
                return Response({"message": "Email Already exists"}, status=status.HTTP_400_BAD_REQUEST)
            if len(data["phone_number"]) != 10:
                return Response({"message": "Phone Number must contains 10 numbers"},
                                status=status.HTTP_400_BAD_REQUEST)
            if queryset.filter(phone_number=data["phone_number"]).exists():
                return Response({"message": "Phone number Already exists"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.serializer_class(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "User Registred Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("register exception", e)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        
class OrganisationRegistrationView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = OrganisationRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"message": "Organization registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WebsiteAccountsUserLoginAPIView(views.APIView):
    def post(self, request):
        try:
            data = request.data
            
            queryset = get_user_model().objects.all()
            if not queryset.filter(email=data["email"]).exists():
                return Response({"message": "Incorrect Credentials"}, status=status.HTTP_400_BAD_REQUEST)
            
            user_query = queryset.get(email=data["email"])
            if not user_query.check_password(data["password"]):
                return Response({"message": "Incorrect Credentials"}, status=status.HTTP_400_BAD_REQUEST)
            
            if user_query.is_active == False:
                return Response({"message": "Your account is not active"}, status=status.HTTP_400_BAD_REQUEST)
            
            if user_query.type_of_user == "ORGANISATION" or user_query.type_of_user == "ENTERPRISE":
                if user_query.is_organisation_admin == False:
                    return Response({"message": "Your account is not approved"}, status=status.HTTP_400_BAD_REQUEST)
                
            data = get_tokens_for_user(user_query)
            data["is_already_login"] = user_query.is_already_login
            data["is_organisation_admin"] = user_query.is_organisation_admin
            user_query.is_already_login = True
            user_query.save()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

