import datetime as dt
import hashlib
import os
import typing as t

from django.conf import settings
from django.db.models import Model
from glamps.constants import TRUE_HANDLER, FALSE_HANDLER

TODAY = dt.date.today()


def hash_value(data: str) -> str:
    return hashlib.md5(str(data).encode()).hexdigest()


def folder_path(instance: Model, filename: str) -> str:
    year_hash = hash_value(TODAY.year)
    month_hash = hash_value(TODAY.month)

    base_upload_path = settings.DEFAULT_FILE_STORAGE

    year_folder = os.path.join(base_upload_path, year_hash)
    month_folder = os.path.join(year_folder, month_hash)

    if not os.path.exists(month_folder):
        os.makedirs(month_folder)

    return os.path.join(year_hash, month_hash, filename)
