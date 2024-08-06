from django.db import models

class OS(models.Model):
    os = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.os

class Setor(models.Model):
    os = models.ForeignKey(OS, related_name='setores', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.os.os} - {self.nome}"

class Etapa(models.Model):
    setor = models.ForeignKey(Setor, related_name='etapas', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.setor.nome} - {self.nome}"

class Imagem(models.Model):
    etapa = models.ForeignKey(Etapa, related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='imagens/')

    def __str__(self):
        return f"{self.etapa.nome} - Imagem"
