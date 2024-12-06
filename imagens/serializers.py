import base64
from rest_framework import serializers
from django.core.files.base import ContentFile

from .models import OS, Sector, Step, Image, StepOs


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'step_os', 'image']

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name']

class StepSerializer(serializers.ModelSerializer):
    sector = SectorSerializer()
    class Meta:
        model = Step
        fields = ['id', 'name', "sector"]

class StepOsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepOs
        fields = ['id', 'step', 'os']


SECTOR_CHOICES =(  
    ("desmontagem", "Desmontagem"),  
    ("montagem", "Montagem"), 
) 

class OSSerializerWrite(serializers.ModelSerializer):
    os = serializers.CharField(required=True, max_length=20)
    sector = serializers.ChoiceField(choices=SECTOR_CHOICES, required=True)
    step = serializers.CharField(required=True)
    images = serializers.ListField()

    class Meta:
        model = OS
        fields = ['id', 'os', 'sector', "step" , "images"]


    def create(self, validated_data):
        sector, _ = Sector.objects.get_or_create(name=validated_data.get("sector"))
        os, created = OS.objects.get_or_create(os=validated_data.get("os"))
        os.sector = sector
        os.save()
        step, _ = Step.objects.get_or_create(name=validated_data.get("step"))
        step_os, _ = StepOs.objects.get_or_create(
            step=step,
            os=os,
        )

        image = validated_data.get("image")
        if image:
            Image.objects.create(step_os=step_os, image=image)

        return os


class OSSerializerRead(serializers.ModelSerializer):
    class Meta:
        model = OS
        fields = ['id', 'os', 'sector']
