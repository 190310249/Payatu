import json


import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "firmwareanalyzer.settings")
django.setup()


with open("nv.json") as fp:
    dir_dict = json.load(fp)


from firmware_manager.models import Directory

Directory.load_from_dict(dir_dict)

