from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(UserModel)
class UserModelModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'id', 'username', 'phone_number', 'type_of_user', 'is_active', 'created_at', 'updated_at', 'is_staff', 'is_organisation_admin', 'is_social_sign_in_user')
    exclude = () 

@admin.register(EmailOtpVerifyModel)
class EmailOtpVerifyModelModelAdmin(admin.ModelAdmin):
    list_display = ('user','email','otp','is_active','created_at','updated_at')
    exclude = ()

@admin.register(OrganisationModel)
class OrganisationModelModelAdmin(admin.ModelAdmin):
    list_display = ('name','admin','domain_name','email_id','address','country','bucket_id','phone_number','url', 'is_approved','is_deleted', 'created_at','updated_at')
    exclude = ()