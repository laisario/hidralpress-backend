import os
from rest_framework import viewsets, response, views, status
from django.core.files.storage import default_storage

from .models import OS, Sector, Step, Image
from .serializers import OSSerializerWrite, OSSerializerRead, SectorSerializer, StepSerializer, ImageSerializer, StepOsSerializer

class OSViewSet(viewsets.ModelViewSet):
    queryset = OS.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "UPDATE"]:
            return OSSerializerWrite
        return OSSerializerRead
    
    def create(self, request, *args, **kwargs):
        serializer = OSSerializerWrite(data=request.data)
        serializer.is_valid()
        os = serializer.save(**serializer.validated_data)
        return response.Response(OSSerializerRead(os).data)
    

class ValidateOSView(views.APIView):
    def post(self, request, format=None):
        os_data = request.data["os"]
        for root, dirs, _ in os.walk(default_storage.location):
                for name in dirs:
                    if os_data == name:
                        return response.Response({"ok": True})

        return response.Response({"ok": False})


class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer

class StepOsViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepOsSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

