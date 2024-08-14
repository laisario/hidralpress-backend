from django.db import models
import os
from django.core.files.storage import default_storage

class OS(models.Model):
    os = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.os
    
class Sectors(models.TextChoices):
    DISASSEMBLY = "desmontagem"
    ASSEMBLY = "montagem"

class Sector(models.Model):
    os = models.ForeignKey(OS, related_name='sectors', on_delete=models.CASCADE)
    name = models.CharField(max_length=11, choices=Sectors.choices)

    def __str__(self):
        return f"{self.os.os} - {self.name}"

class Steps(models.TextChoices):
    ARRIVAL = "chegada"
    DISASSEMBLED = "desmontado"
    READY = "pronto"
    ASSEMBLY = "montagem"
    TEST = "teste"

class Step(models.Model):
    sector = models.ForeignKey(Sector, related_name='steps', on_delete=models.CASCADE)
    name = models.CharField(max_length=12, choices=Steps.choices)

    def __str__(self):
        return f"{self.sector.name} - {self.name}"

def upload_to_server(instance, filename):
    os_path = None
    for root, dirs, _ in os.walk(default_storage.location):
            for name in dirs:
                if instance.step.sector.os.os == name:
                    os_path = os.path.join(root, name)

    if not os_path:
        raise Exception
    step_path = os_path + "/" + instance.step.name
    if not os.path.exists(step_path):
        os.mkdir(step_path)
    return os.path.relpath(f"{step_path}/{filename}", default_storage.location)

class Image(models.Model):
    step = models.ForeignKey(Step, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_server)

    def __str__(self):
        return f"{self.step.name} - Image"
