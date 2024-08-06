from rest_framework import viewsets
from .models import OS, Setor, Etapa, Imagem
from .serializers import OSSerializer, SetorSerializer, EtapaSerializer, ImagemSerializer

class OSViewSet(viewsets.ModelViewSet):
    queryset = OS.objects.all()
    serializer_class = OSSerializer

class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer

class EtapaViewSet(viewsets.ModelViewSet):
    queryset = Etapa.objects.all()
    serializer_class = EtapaSerializer

class ImagemViewSet(viewsets.ModelViewSet):
    queryset = Imagem.objects.all()
    serializer_class = ImagemSerializer

