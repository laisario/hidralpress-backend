import os
from django.db import models
from django.core.files.storage import default_storage
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from imagekit.models import ImageSpecField
from imagekit.cachefiles.strategies import JustInTime
from imagekit.processors import ResizeToFill

class Sectors(models.TextChoices):
    DISASSEMBLY = "desmontagem", _("Desmontagem")
    ASSEMBLY = "montagem", _("Montagem")

class Sector(models.Model):
    name = models.CharField(max_length=11, choices=Sectors.choices)
    def __str__(self):
            return self.name


class Steps(models.TextChoices):
    ARRIVAL = "C-EQUIPAMENTO", _("Chegada")
    DISASSEMBLED = "E-DESMONTADO", _("Desmontado")
    READY = "E-PRONTO", _("Pronto")
    ASSEMBLY = "E-MONTAGEM", _("Montagem")
    TEST = "E-TESTE", _("Teste")

class Step(models.Model):
    name = models.CharField(max_length=15, choices=Steps.choices)
    sector = models.ForeignKey(Sector, related_name="step", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class OS(models.Model):
    os = models.CharField(max_length=100, unique=True, db_index=True)
    path = models.CharField(max_length=1024, unique=True, db_index=True, null=True, blank=True)
    sector = models.ForeignKey(Sector, related_name="os", null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.os


class StepOs(models.Model):
    step = models.ForeignKey(Step, related_name='step_os', on_delete=models.CASCADE)
    os = models.ForeignKey(OS, related_name='step_os', on_delete=models.CASCADE)

    
def upload_to_server(instance, filename):
    os_path = instance.step_os.os.path
    if not os_path:
        raise Exception("A pasta da OS não existe!")
    step_path = os_path + "/" + instance.step_os.step.name
    if not os.path.exists(step_path):
        os.mkdir(step_path)
    return os.path.relpath(f"{step_path}/{filename}", default_storage.location)


class Image(models.Model):
    step_os = models.ForeignKey(StepOs, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_server, max_length=1000)
    thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(640, 360)], format='JPEG', options={'quality': 60}, cachefile_strategy=JustInTime())
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.step_os.step.name} - Image {self.pk}"
    