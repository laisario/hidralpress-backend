import os
from rest_framework import viewsets, response, views, status
from django.core.files.storage import default_storage
from django.core.cache import cache
from rest_framework.decorators import action
from .models import OS, Sector, Step, Image
from .serializers import OSSerializerWrite, OSSerializerRead, SectorSerializer, StepSerializer, ImageSerializer, StepOsSerializer
import subprocess
import threading
from rest_framework.response import Response


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
    
    @action(detail=False, methods=['post'])
    def execute_update_os(self, request):
        cache.set("update_os_progress", "started")
        threading.Thread(target=self.run_update_os).start()
        return Response({"status": "ok"})

    def run_update_os(self):
        update_os = ["python", "manage.py", "update_os"]
        process = subprocess.Popen(update_os, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        process.wait()


class ValidateOSView(views.APIView):
    def post(self, request, format=None):
        return response.Response({"ok": OS.objects.filter(os=request.data["os"]).exists()})


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

