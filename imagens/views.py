import os
import re
from rest_framework import viewsets, response, views, status
from .models import OS, Sector, Step, Image
from .serializers import OSSerializerWrite, OSSerializerRead, SectorSerializer, StepSerializer, ImageSerializer, StepOsSerializer
from datetime import date
from django.core.files.storage import default_storage


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
        current_year = date.today().year
        time_available = current_year - 1
        year_available = str(time_available)[2:]
        os = request.data["os"]

        year = os[7:9]

        if year < year_available:
            return response.Response({"ok": False, "msg": 'Ano indisponível para tirar foto'})
        return response.Response({"ok": OS.objects.filter(os=os).exists()})
    

class UpdateAllOSView(views.APIView):
    def post(self, request, format=None):
        file_data = request.body.decode('utf-8')
        lines = file_data.strip().splitlines()
        
        record_dict = {}
        for line in lines:
            match = re.search("OS [0-9]+-[0-9]+", line)
            if match:
                os_value = line[match.span()[0]:match.span()[1]]
                record_dict[os_value] = line
        records = [OS(os=os_key, path=path) for os_key, path in record_dict.items()]
        OS.objects.bulk_create(records, update_conflicts=True, unique_fields=['os'], update_fields=['path'])
        
        return response.Response({"status": "success", "message": "Data uploaded successfully"}, status=status.HTTP_201_CREATED)


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
    serializer_class = ImageSerializer
     
    def get_queryset(self):
        step_name = self.request.query_params.get('step', None)
        os_identifier = self.request.query_params.get('os', None)

        if step_name and os_identifier:
            return Image.objects.filter(
                step_os__step__name=step_name,
                step_os__os__os=os_identifier
            ).reverse()
        
        return Image.objects.none()
    
    def destroy(self, request, *arg, **kwargs):
        instance = self.get_object()

        image_path = instance.image.path
        print("achar", instance.image)
        print("achar", instance.image.name)
        print("achar", instance.image.path)
        print("achar", instance.image.url)   
 
        if os.path.exists(image_path):
            default_storage.delete(image_path)

        instance.delete()

        return response.Response({"detail": "Imagem deletada com sucesso."}, status=status.HTTP_204_NO_CONTENT)    


