from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import Imagem, Setor, Etapa, OS


@admin.register(Imagem)
class ImagemAdmin(admin.ModelAdmin):
    list_display = ("id", "etapa", "imagem")


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ("id", "os", "nome")

@admin.register(Etapa)
class EtapaAdmin(admin.ModelAdmin):
    list_display = ("id", "setor", "nome")

@admin.register(OS)
class OSAdmin(admin.ModelAdmin):
    list_display = ("id", "os")

admin.site.unregister(Group)
admin.site.index_title = _("Painel Administrativo")
admin.site.site_header = _("Hidralpress")
admin.site.site_title = _("Hidralpress")

