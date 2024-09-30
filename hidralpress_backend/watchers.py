import os
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers.read_directory_changes import WindowsApiObserver
import re
from imagens.models import OS

class DirectoryHandler(FileSystemEventHandler):
    def on_created(self, event):
        regex_match = re.search("OS [0-9]+-[0-9]+", event.src_path)
        if event.is_directory and regex_match:
            os_number = event.src_path[regex_match.span()[0]:regex_match.span()[1]]
            saved_os = OS.objects.filter(os=os_number)
            if saved_os.exists():
                saved_os = saved_os.first()
                saved_os.path = event.src_path
                saved_os.save()
            else:
                OS.objects.create(os=os_number, path=event.src_path)

        

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
        path = "Z:"
        if not cls._watching:
            event_handler = DirectoryHandler()
            observer = WindowsApiObserver()
            observer.schedule(event_handler, path=path, recursive=False)
            observer.start()

            cls._watching = True