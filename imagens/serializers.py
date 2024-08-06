from rest_framework import serializers
from .models import OS, Setor, Etapa, Imagem


class ImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagem
        fields = ['id', 'etapa', 'imagem']

class EtapaSerializer(serializers.ModelSerializer):
    imagens = ImagemSerializer(many=True)
    class Meta:
        model = Etapa
        fields = ['id', 'setor', 'nome', 'imagens']

class SetorSerializer(serializers.ModelSerializer):
    etapas = EtapaSerializer(many=True)
    class Meta:
        model = Setor
        fields = ['id', 'os', 'nome', 'etapas']

class OSSerializer(serializers.ModelSerializer):
    setores = SetorSerializer(many=True)
    class Meta:
        model = OS
        fields = ['id', 'os', 'setores']
