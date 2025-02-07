import hashlib
from datetime import datetime
import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from config import settings


class ThumbnailStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        filename = os.path.basename(name)

        now = datetime.now()
        new_path = os.path.join("images", now.strftime("%Y/%m-%d"), "thumbs", filename)

        return super().get_available_name(new_path, max_length)


def upload_to(instance, filename):
    now = datetime.now()
    year = now.strftime("%Y")
    month_day = now.strftime("%m-%d")

    ext = os.path.splitext(filename)[1]
    hash_name = hashlib.md5(filename.encode()).hexdigest()

    unique_filename = f"{hash_name}{ext}"

    return os.path.join("images", year, month_day, unique_filename)


def process_image(image):
    if image:
        img = Image.open(image)
        ext = os.path.splitext(image.name)[1]

        if ext in [".png", ".webp"]:
            img = img.convert("RGB")
            ext = ".jpg"
            img_format  = "JPEG"
        else:
            img_format  = img.format

        output = BytesIO()
        img.save(output, format=img_format, quality=settings.QUALITY_IMAGE, optimize=True)
        output.seek(0)

        return ContentFile(output.read(), name=f"compressed_{image.name}{ext}")
    return None