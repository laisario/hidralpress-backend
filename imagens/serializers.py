from rest_framework import serializers
from .models import OS, Setor, Etapa, Imagem

class OSSerializer(serializers.ModelSerializer):
    class Meta:
        model = OS
        fields = ['id', 'os']

class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = ['id', 'os', 'nome']

class EtapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etapa
        fields = ['id', 'setor', 'nome']

class ImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagem
        fields = ['id', 'etapa', 'imagem']