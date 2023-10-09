from rest_framework import serializers
from .models import Firmware
from user_auth.models import OrganisationModel

class FirmwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firmware
        fields = ['name','hash','md5','sha1','sha256','location']
    def validate(self, attrs):
        if not "location" in attrs:
            raise serializers.ValidationError("File Not Found")
        else:
            return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['admin'] = user
        admin_org = OrganisationModel.objects.get(admin=user)
        validated_data['admin_org'] = admin_org
        if "location" in validated_data:
            location = validated_data.pop('location')
            Firmware.objects.create(location=self.context['request'].FILES.get('location'), **validated_data)
            return validated_data
        else:
            pass
        
class UserFirmwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firmware
        fields = ['uuid','name', 'hash', 'md5', 'sha1', 'sha256', 'location', 'created', 'modified']

