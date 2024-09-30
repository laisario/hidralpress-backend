from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from imagens.models import OS
import re
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        for root, dirs, _ in os.walk(default_storage.location):
            for dir in dirs:
                path = os.path.join(root, dir)
                regex_match = re.search("OS [0-9]+-[0-9]+", dir)
                if regex_match:
                    os_number = dir[regex_match.span()[0]:regex_match.span()[1]]
                    saved_os = OS.objects.filter(os=os_number)
                    if saved_os.exists():
                        saved_os = saved_os.first()
                        saved_os.path = path
                        saved_os.save()
                    else:
                        OS.objects.create(os=os_number, path=path)
