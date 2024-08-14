from rest_framework import serializers
from .models import OS, Sector, Step, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'step', 'image']

class StepSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    class Meta:
        model = Step
        fields = ['id', 'sector', 'name', 'images']

class SectorSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)
    class Meta:
        model = Sector
        fields = ['id', 'os', 'name', 'steps']

class OSSerializer(serializers.ModelSerializer):
    sectors = SectorSerializer(many=True)
    class Meta:
        model = OS
        fields = ['id', 'os', 'sectors']
