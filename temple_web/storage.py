from urllib.parse import urljoin

from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class DynamicStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # Delete existing file if it exists
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

# class AbsolutePathStorage(FileSystemStorage):
#     def url(self, name):
#         """Returns absolute URL including MEDIA_URL"""
#         if not name:
#             return ''
#         if self.base_url is None:
#             raise ValueError("This file is not accessible via a URL.")
#         return urljoin(settings.MEDIA_URL, name)
#
# dynamic_storage = AbsolutePathStorage()