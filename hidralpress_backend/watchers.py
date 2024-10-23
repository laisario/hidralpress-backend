from watchdog.events import FileSystemEventHandler
from django.core.files.storage import default_storage

from platform import system
if system() == 'Windows':
    from watchdog.observers.read_directory_changes import WindowsApiObserver as Observer
else:
    from watchdog.observers import Observer
import re
from imagens.models import OS

class DirectoryHandler(FileSystemEventHandler):
    def on_moved(self, event):
        regex_match = re.search("OS [0-9]+-[0-9]+", event.dest_path)
        if event.is_directory and regex_match:
            os_number = event.dest_path[regex_match.span()[0]:regex_match.span()[1]]
            saved_os = OS.objects.filter(os=os_number)
            if saved_os.exists():
                saved_os = saved_os.first()
                saved_os.path = event.dest_path
                saved_os.save()
            else:
                OS.objects.create(os=os_number, path=event.dest_path)
    
    def on_deleted(self, event):
        regex_match = re.search("OS [0-9]+-[0-9]+", event.src_path)
        print(event.src_path, regex_match, 'aaaaaaaaa')
        if regex_match:
            os_number = event.src_path[regex_match.span()[0]:regex_match.span()[1]]
            print(os_number in event.src_path, 'cccccccccc')
            print(os_number, event.src_path.endswith(os_number), 'bbbbbbbbbbbbb')
            if event.is_directory and os_number in event.src_path:
                saved_os = OS.objects.filter(os=os_number)
                if saved_os.exists():
                    saved_os = saved_os.first()
                    saved_os.delete()

        

class FileWatcher(object):
    _instance = None
    _watching = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            print("Creating new FileWatcher")
            cls._instance = super(FileWatcher, cls).__new__(cls, *args, **kwargs)

            cls.start_watching()

        return cls._instance

    @classmethod
    def start_watching(cls):
        path = default_storage.location
        if not cls._watching:
            event_handler = DirectoryHandler()
            observer = Observer()
            observer.schedule(event_handler, path=path, recursive=True)
            observer.start()

            cls._watching = True