import os
from django.core.files import File
from django.core.files.storage import FileSystemStorage

class MyFileSystemStorage(FileSystemStorage):
    def save(self, name, content, max_length=None):
        if name is None:
            name = content.name

        if not hasattr(content, "chunks"):
            content = File(content, name)

        name = self._save(name, content)
        return name