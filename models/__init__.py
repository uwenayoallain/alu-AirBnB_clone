"""Initialize the models package and set up storage.

Creates a single `FileStorage` instance and reloads any persisted objects.
"""
from models.engine import file_storage

storage = file_storage.FileStorage()
storage.reload()
