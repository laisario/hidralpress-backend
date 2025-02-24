from rest_framework import serializers
from django.conf import settings
from .models import OS, Sector, Step, Image, StepOs, Video


class ImageSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'step_os', 'image', 'thumbnail', 'created_at']

    def get_thumbnail(self, obj):
        url = settings.BACK_URL + obj.thumbnail.url
        return url


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'step_os', 'video', 'created_at']


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


class OSSerializerWrite(serializers.Serializer):
    os = serializers.CharField(required=True, max_length=20)
    sector = serializers.ChoiceField(choices=SECTOR_CHOICES, required=True)
    step = serializers.CharField(required=True)
    image = serializers.FileField(max_length=None, allow_empty_file=True, use_url=True, required=False)
    video = serializers.FileField(max_length=None, allow_empty_file=True, use_url=True, required=False)

    def create(self, validated_data):
        sector, _ = Sector.objects.get_or_create(name=validated_data["sector"])
        os, created = OS.objects.get_or_create(os=validated_data["os"])
        os.sector = sector
        os.save()

        step, _ = Step.objects.get_or_create(name=validated_data["step"])
        step_os, _ = StepOs.objects.get_or_create(
            step=step,
            os=os,
        )

        image = validated_data.get('image', None)
        video = validated_data.get('video', None)
        if image:
            Image.objects.create(step_os=step_os, image=image)
        elif video:
            Video.objects.create(step_os=step_os, video=video)

        return {
            "os": os.os,
            "sector": sector.name,
            "step": step.name,
            "image": image.url if image else None,
            "video": video.url if video else None
        }

class OSSerializerRead(serializers.ModelSerializer):
    class Meta:
        model = OS
        fields = ['id', 'os', 'sector']
