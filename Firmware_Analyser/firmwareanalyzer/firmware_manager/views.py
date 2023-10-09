from django.shortcuts import render
from rest_framework import generics, views, pagination, permissions, authentication
from .models import Firmware
from .serializers import *
from rest_framework.response import Response
from rest_framework import status

class FirmwareCreateView(generics.CreateAPIView):
    queryset = Firmware.objects.all()
    serializer_class = FirmwareSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # authenticate_class = [authentication.SessionAuthentication, authentication.BasicAuthentication,
    #                       authentication.TokenAuthentication, authentication.BaseAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "Firmware Uploaded Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class UserFirmwareListView(generics.ListAPIView):
    serializer_class = UserFirmwareSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Firmware.objects.filter(admin_id=user_id)
    
class UserFirmwareDetailView(generics.RetrieveAPIView):
    serializer_class = UserFirmwareSerializer
    # permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'uuid'  # Set the lookup field to 'uuid'

    def get_queryset(self):
        uuid = self.kwargs['uuid']
        return Firmware.objects.filter(uuid=uuid)
