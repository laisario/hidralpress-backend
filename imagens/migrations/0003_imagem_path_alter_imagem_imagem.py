# Generated by Django 4.2 on 2024-08-14 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagens', '0002_alter_etapa_nome_alter_setor_nome'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagem',
            name='path',
            field=models.FilePathField(default='/home/laisarva/hidralpress-prod'),
        ),
        migrations.AlterField(
            model_name='imagem',
            name='imagem',
            field=models.ImageField(upload_to='tmp'),
        ),
    ]
