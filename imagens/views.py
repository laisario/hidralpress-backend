import os
from rest_framework import viewsets, response, views, status
from django.core.files.storage import default_storage
from django.core.cache import cache
from rest_framework.decorators import action
from .models import OS, Sector, Step, Image
from .serializers import OSSerializerWrite, OSSerializerRead, SectorSerializer, StepSerializer, ImageSerializer, StepOsSerializer
from hidralpress_backend.watchers import on_created, on_deleted
import subprocess
import threading
import re
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
        update_os = ["/scan_dirs.sh"]
        process = subprocess.Popen(update_os, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        process.wait()


class ValidateOSView(views.APIView):
    def post(self, request, format=None):
        return response.Response({"ok": OS.objects.filter(os=request.data["os"]).exists()})
    

class UpdateAllOSView(views.APIView):
    def post(self, request, format=None):
        file_data = request.body.decode('utf-8')
        lines = file_data.strip().splitlines()
        
        records = []
        for line in lines:
            match = re.search("OS [0-9]+-[0-9]+", line)
            record = OS(
                os=line[match.span()[0]:match.span()[1]],
                path=line,
            )
            records.append(record)
        OS.objects.bulk_create(records, ignore_conflicts=True)
        
        return Response({"status": "success", "message": "Data uploaded successfully"}, status=status.HTTP_201_CREATED)


class UpdateOnEventView(views.APIView):
    def post(self, request, format=None):
        event_type = request.data["type"]
        path = request.data["path"]
        if event_type == "created" or event_type == "renamed":
            on_created(path)
        elif event_type == "deleted":
            on_deleted(path)
        return response.Response({"ok": True})


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

