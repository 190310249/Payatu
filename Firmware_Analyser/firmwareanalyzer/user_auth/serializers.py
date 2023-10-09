from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from .token import get_tokens_for_user
from collections import OrderedDict


# Serializer for user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "phone_number", "email", "password"]

    def validate(self, data):
        if get_user_model().objects.filter(email=data["username"]).exists():
            raise serializers.ValidationError({
                "message": "Username Already Exists"
            })
        if get_user_model().objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({
                "message": "Email Already Exists"
            })
        if len(data["phone_number"]) != 10:
            raise serializers.ValidationError({
                "message": "phone Number must contains 10 digits only"
            })
        if get_user_model().objects.filter(phone_number=data["phone_number"]).exists():
            raise serializers.ValidationError({
                "message": "Phone Number Already Exists"
            })
        return data

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            phone_number=validated_data["phone_number"]
        )
        user.set_password(validated_data["password"])
        user.is_organisation_admin = False
        user.type_of_user = "INDIVIDUAL"
        user.save()

        return validated_data
    
# Serializer for ORGANISATION/ENTERPRISE registration
class OrganisationRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    domain_name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ["username", "phone_number", "email", "password", "type_of_user", "domain_name", "address", "country"]

    def validate(self, data):
        data1 = self.context['request'].data
        data = OrderedDict(data1.items())
        if get_user_model().objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError({
                "message": "Organisation Name Already Exists"
            })
        if get_user_model().objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({
                "message": "Organisation Email Already Exists"
            })
        if len(data["phone_number"]) != 10:
            raise serializers.ValidationError({
                "message": "Phone Number must contain 10 digits only"
            })
        if get_user_model().objects.filter(phone_number=data["phone_number"]).exists():
            raise serializers.ValidationError({
                "message": "Phone Number Already Exists"
            })
        return data

    def create(self, validated_data):
        # Create a new user
        # print("validated_data", validated_data)
        user = get_user_model().objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            phone_number=validated_data["phone_number"]
        )
        user.set_password(validated_data["password"])
        user.type_of_user = validated_data["type_of_user"]
        user.save()

        # Create a corresponding organization entry
        organization = OrganisationModel(
            admin=user,
            name=validated_data.get("username"),
            domain_name=validated_data.get("domain_name"),
            email_id=validated_data.get("email"),
            phone_number=validated_data.get("phone_number"),
            address=validated_data.get("address"),
            country=validated_data.get("country"),
        )
        organization.is_approved = False  # Set is_approved to False by default
        organization.save()

        return validated_data


class WebsitUserLoginSerializer():
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        return get_tokens_for_user
