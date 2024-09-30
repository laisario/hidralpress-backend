from django.db import models
import os
from django.core.files.storage import default_storage
from django.utils.translation import gettext_lazy as _

class Sectors(models.TextChoices):
    DISASSEMBLY = "desmontagem", _("Desmontagem")
    ASSEMBLY = "montagem", _("Montagem")

class Sector(models.Model):
    name = models.CharField(max_length=11, choices=Sectors.choices)
    def __str__(self):
            return self.name


class Steps(models.TextChoices):
    ARRIVAL = "chegada", _("Chegada")
    DISASSEMBLED = "desmontado", _("Desmontado")
    READY = "pronto", _("Pronto")
    ASSEMBLY = "montagem", _("Montagem")
    TEST = "teste", _("Teste")

class Step(models.Model):
    name = models.CharField(max_length=12, choices=Steps.choices)
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
    os_path = instance.os.path
    if not os_path:
        raise Exception("A pasta da OS não existe!")
    step_path = os_path + "/" + instance.step_os.step.name
    if not os.path.exists(step_path):
        os.mkdir(step_path)
    return os.path.relpath(f"{step_path}/{filename}", default_storage.location)


class Image(models.Model):
    step_os = models.ForeignKey(StepOs, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_server)

    def __str__(self):
        return f"{self.step_os.step.name} - Image"
