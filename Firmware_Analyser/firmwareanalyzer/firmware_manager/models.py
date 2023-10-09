import itertools
import os
import uuid
from user_auth.models import *
from django.db import models
from django.db.models.aggregates import Case, When
from rich import print as eprint
import hashlib
from django.contrib.auth import get_user_model

BUF_SIZE = 65536

class FirmwareStatusEnum(models.TextChoices):
    SUBMITTED = "submitted"
    FAILED = "failed"
    RUNNING = "running"
    DONE = "done"



def firmware_upload_location(instance, filename):
    # Generate a UUID for the file's name
    filename = str(instance.uuid)

    # Return the file path
    return os.path.join("firmwares", filename)


class Firmware(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    # project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True)
    admin = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # assessment = models.ForeignKey('Assessment', on_delete=models.CASCADE)
    root_dir = models.ForeignKey("Directory", on_delete=models.CASCADE, blank=True, null=True)
    admin_org = models.ForeignKey(OrganisationModel, on_delete=models.CASCADE, related_name="firmwares", blank=True, null=True)
    shared_orgs = models.ManyToManyField(OrganisationModel, related_name="shared_firmwares", blank=True)    
    hash = models.CharField(max_length=64, blank=True, null=True)
    file_size  = models.PositiveIntegerField(blank=True, null=True)
    file_type = models.CharField(max_length=255, blank=True, null=True)
    md5 = models.CharField(max_length=32, blank=True, null=True)
    sha1 = models.CharField(max_length=40, blank=True, null=True)
    sha256 = models.CharField(max_length=64, blank=True, null=True)
    location = models.FileField(upload_to=firmware_upload_location)
    status = models.CharField(max_length=255, choices=FirmwareStatusEnum.choices, default=FirmwareStatusEnum.SUBMITTED)
    failure_reason = models.TextField(null=True, blank=True)    
    is_deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)




# Create your models here.


class RawFile(models.Model):
    owner = models.IntegerField()
    group = models.IntegerField()
    setuid = models.BooleanField()
    sticky = models.BooleanField()
    perms = models.IntegerField()
    created = models.BigIntegerField()
    modified = models.BigIntegerField()
    islink = models.BooleanField()
    size = models.IntegerField()
    mime = models.CharField(max_length=255)
    magic = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Directory(models.Model):
    """Class to hold directories"""

    owner = models.IntegerField()
    group = models.IntegerField()
    setuid = models.BooleanField()
    sticky = models.BooleanField()
    perms = models.IntegerField()
    created = models.BigIntegerField()
    modified = models.BigIntegerField()
    islink = models.BooleanField()
    size = models.IntegerField()
    mime = models.CharField(max_length=255)
    magic = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    parent = models.ForeignKey(
        "Directory", on_delete=models.CASCADE, default=None, blank=True, null=True
    )
    name = models.CharField(max_length=255)

    rname = models.CharField(max_length=255, default="", blank=True)
    rparent = models.CharField(max_length=255, default="", blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    DIR2CREATE = []
    FILES2CREATE = []

    def __init__(self, *args, **kwargs):
        # real path for the first Node storing the real parent directory
        self._path, self._rpath = None, None
        super().__init__(*args, **kwargs)

    @property
    def directories(self):
        """The directories property."""
        return list(Directory.objects.filter(parent=self.uuid))

    @property
    def files(self):
        """The file property."""
        return list(File.objects.filter(parent=self.uuid))

    @staticmethod
    def load_from_dict(dir_dict, root=True):
        """ """
        d = Directory()
        d.owner = dir_dict["owner"]
        d.group = dir_dict["group"]
        d.setuid = dir_dict["setuid"]
        d.sticky = dir_dict["sticky"]
        d.perms = dir_dict["perms"]
        d.created = dir_dict["created"]
        d.modified = dir_dict["modified"]
        d.islink = dir_dict["islink"]
        d.size = dir_dict["size"]
        d.mime = dir_dict["mime"]
        d.magic = dir_dict["magic"]
        d.uuid = dir_dict["uuid"]
        d.rname = dir_dict["rname"]
        d.rparent = dir_dict["rparent"]
        # d.parent = Directory.objects.get(uuid=dir_dict["parent"]) if dir_dict["parent"] else None
        d.name = dir_dict["name"]

        subdirs, subfiles, subdir_relation, subfiles_relation = (
            [d],
            [],
            [(dir_dict["parent"], d.uuid)],
            [],
        )
        for directory in dir_dict["directories"]:
            (
                _subdirs,
                _subfiles,
                _subdir_relation,
                _subfile_relation,
            ) = Directory.load_from_dict(directory, root=False)
            subdirs += _subdirs
            subfiles += _subfiles
            subdir_relation += _subdir_relation
            subfiles_relation += _subfile_relation

        for file in dir_dict["files"]:
            fobj, frel = File.load_from_dict(file)
            subfiles.append(fobj)
            subfiles_relation.append(frel)

        if not root:
            return subdirs, subfiles, subdir_relation, subfiles_relation

        d_relations = {}
        for entry in subdir_relation:
            if entry[0] in d_relations:
                d_relations[entry[0]].append(entry[1])
            else:
                d_relations[entry[0]] = [entry[1]]

        f_relations = {}
        for entry in subfiles_relation:
            if entry[0] in f_relations:
                f_relations[entry[0]].append(entry[1])
            else:
                f_relations[entry[0]] = [entry[1]]

        Directory.objects.bulk_create(subdirs)
        File.objects.bulk_create(subfiles)

        # Fetch all directory and file objects in one query each
        # eprint(d_relations.keys())
        all_directories = Directory.objects.in_bulk(
            list(itertools.chain(*d_relations.values()))
        )
        all_files = File.objects.in_bulk(list(itertools.chain(*f_relations.values())))

        all_directories = {str(key): value for key, value in all_directories.items()}
        all_files = {str(key): value for key, value in all_files.items()}

        # Update all the directories and files with their respective parent values
        for parent_uuid, child_uuids in d_relations.items():
            if parent_uuid:
                for child_uuid in child_uuids:
                    all_directories[child_uuid].parent = all_directories[parent_uuid]
        Directory.objects.bulk_update(list(all_directories.values()), ["parent"])

        for parent_uuid, child_uuids in f_relations.items():
            for child_uuid in child_uuids:
                all_files[child_uuid].parent = all_directories[parent_uuid]
        File.objects.bulk_update(list(all_files.values()), ["parent"])

        # # Update the parent field of directories
        # for parent_uuid, child_uuids in d_relations.items():
        #     Directory.objects.filter(uuid__in=child_uuids).update(parent=parent_uuid)
        #
        # # Update the parent field of files (if needed)
        # for parent_uuid, child_uuids in f_relations.items():
        #     File.objects.filter(uuid__in=child_uuids).update(parent=parent_uuid)

    @property
    def path(self):
        """returns the path relative to the starting node"""
        if self._path is None:
            parent_path = self.parent.path if self.parent else ""
            self._path = os.path.join(parent_path, self.name)

        return self._path

    @property
    def rpath(self):
        """returns the real path to the dir/file on disk useful if you want to interact"""
        if self._rpath is None:
            # print(f"{self.parent}::{self.rparent}::{self.rname}")
            if self.parent:
                parent_rpath = self.parent.rpath
                self._rpath = os.path.join(parent_rpath, self.name)
            else:
                self._rpath = os.path.join(self.rparent, self.rname)
        return self._rpath

    def flat(self, files=True, dirs=True, use_real_path=False, objs=False):
        """
        Return a list of all files and/or directories
        within the directory and its subdirectories
        """
        all_entries = []

        def traverse(directory):
            if files:
                all_entries.extend(directory.files.all())
            if dirs:
                all_entries.extend(directory.directories.all())
            for subdirectory in directory.directories.all():
                traverse(subdirectory)

        traverse(self)

        if use_real_path:
            res = {entry.rpath: entry for entry in all_entries}
        else:
            res = {entry.path: entry for entry in all_entries}

        return res if objs else list(res.keys())

    def get(self, path):
        path_parts = path.split(os.sep)
        current_dir = self
        for part in path_parts[:-1]:
            if not part:
                continue
            found_entry = None
            for entry in current_dir.directories.all():
                if entry.name == part:
                    found_entry = entry
                    break
            if not found_entry:
                return None
            current_dir = found_entry

        target = path_parts[-1]
        for entry in current_dir.files.all() + current_dir.directories.all():
            if entry.name == target:
                return entry

        return None

    def search(self, name):
        """Search for a file or folder within the directory and all its subdirectories"""
        all_entries = []
        all_entries.extend(self.files.all())
        all_entries.extend(self.directories.all())

        result = []
        for entry in all_entries:
            if name in entry.name:
                result.append(entry.path)
            if isinstance(entry, Directory):
                result.extend(entry.search(name))

        return result

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name


class File(models.Model):
    """Class to hold files"""

    owner = models.IntegerField()
    group = models.IntegerField()
    setuid = models.BooleanField()
    sticky = models.BooleanField()
    perms = models.IntegerField()
    created = models.BigIntegerField()
    modified = models.BigIntegerField()
    islink = models.BooleanField()
    size = models.IntegerField()
    mime = models.CharField(max_length=255)
    magic = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "Directory", on_delete=models.CASCADE, default=None, blank=True, null=True
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def load_from_dict(file_dict):
        """ """
        f = File()
        f.owner = file_dict["owner"]
        f.group = file_dict["group"]
        f.setuid = file_dict["setuid"]
        f.sticky = file_dict["sticky"]
        f.perms = file_dict["perms"]
        f.created = file_dict["created"]
        f.modified = file_dict["modified"]
        f.islink = file_dict["islink"]
        f.size = file_dict["size"]
        f.mime = file_dict["mime"]
        f.magic = file_dict["magic"]
        f.uuid = file_dict["uuid"]
        f.parent = None
        f.name = file_dict["name"]
        return f, (file_dict["parent"], f.uuid)

    @property
    def path(self):
        """returns the path relative to the starting node"""
        if isinstance(self.parent, str):
            return self.parent

        if self.parent:
            path = os.path.join(self.parent.path, self.name)
            return path

    @property
    def rpath(self):
        """returns the real path to the dir/file on disk useful if you want to interact"""

        if isinstance(self.parent, str):
            return self.parent

        path = os.path.join(self.parent.rpath, self.name)
        return path

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name
