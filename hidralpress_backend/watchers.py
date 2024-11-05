import re
from imagens.models import OS

def on_created(path):
    regex_match = re.search("OS [0-9]+-[0-9]+", path)
    if regex_match:
        os_number = path[regex_match.span()[0]:regex_match.span()[1]]
        saved_os = OS.objects.filter(os=os_number)
        if saved_os.exists():
            saved_os = saved_os.first()
            saved_os.path = path
            saved_os.save()
        else:
            OS.objects.create(os=os_number, path=path)

def on_deleted(path):
    regex_match = re.search("OS [0-9]+-[0-9]+", path)
    if regex_match:
        os_number = path[regex_match.span()[0]:regex_match.span()[1]]
        if os_number in path:
            saved_os = OS.objects.filter(os=os_number)
            if saved_os.exists():
                saved_os = saved_os.first()
                saved_os.delete()
