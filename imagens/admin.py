from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import Image, Sector, Step, OS, StepOs


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "step_os", "image")


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'sector')

@admin.register(StepOs)
class StepOsAdmin(admin.ModelAdmin):
    list_display = ("id", "step", "os")

@admin.register(OS)
class OSAdmin(admin.ModelAdmin):
    list_display = ("id", "os", "sector")

admin.site.unregister(Group)
admin.site.index_title = _("Painel Administrativo")
admin.site.site_header = _("Hidralpress")
admin.site.site_title = _("Hidralpress")

