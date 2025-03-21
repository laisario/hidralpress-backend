from rest_framework import serializers
from django.conf import settings
from .models import OS, Sector, Step, Image, StepOs, Video


class ImageSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'step_os', 'image', 'thumbnail', 'created_at']

    def get_thumbnail(self, obj):
        url = settings.BACK_URL + obj.thumbnail.url
        return url
    
    def get_image(self, obj):
        url = settings.BACK_URL + obj.image.url
        return url


class VideoSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'step_os', 'video', 'created_at']
    
    def get_video(self, obj):
        url = settings.BACK_URL + obj.video.url
        return url


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
    image = serializers.FileField(write_only=True, max_length=None, allow_empty_file=True, use_url=True, required=False)
    video = serializers.FileField(write_only=True, max_length=None, allow_empty_file=True, use_url=True, required=False)
    image_response = ImageSerializer(read_only=True, required=False)
    video_response = VideoSerializer(read_only=True, required=False)

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
            image = Image.objects.create(step_os=step_os, image=image)
        if video:
            video = Video.objects.create(step_os=step_os, video=video)

        return {
            "os": os.os,
            "sector": sector.name,
            "step": step.name,
            "image_response": image if image else None,
            "video_response": video if video else None
        }

class OSSerializerRead(serializers.ModelSerializer):
    class Meta:
        model = OS
        fields = ['id', 'os', 'sector']


class ContentSerializer(serializers.Serializer):
    image = ImageSerializer(required=False, many=False)
    video = VideoSerializer(required=False, many=False)

    def to_representation(self, instance):
        if isinstance(instance, Image):
            return {"image": ImageSerializer(instance).data}
        if isinstance(instance, Video):
            return {"video": VideoSerializer(instance).data}
        return super().to_representation(instance)
