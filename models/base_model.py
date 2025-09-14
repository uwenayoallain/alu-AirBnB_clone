#!/usr/bin/python3
"""Defines the `BaseModel` class with common attributes/methods.

This class provides:
- `id`: unique string identifier (UUID4)
- `created_at`: datetime of instance creation
- `updated_at`: datetime of last update
- `save()`: updates `updated_at` and delegates persistence to storage
- `to_dict()`: serializes attributes with ISO-formatted datetimes and `__class__`
"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Defines common attributes/methods for other classes."""

    def __init__(self, *args, **kwargs):
        """Initialize a new instance.

        If `kwargs` are provided, use them to set attributes, converting
        `created_at` and `updated_at` from ISO strings. Otherwise, generate
        defaults and register the instance with storage.
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"

        if kwargs:
            # Avoid persisting the __class__ marker on instances
            kwargs.pop("__class__", None)

            # Convert date strings back to datetime objects when present
            created = kwargs.get("created_at")
            updated = kwargs.get("updated_at")
            if isinstance(created, str):
                kwargs["created_at"] = datetime.strptime(created, time_format)
            if isinstance(updated, str):
                kwargs["updated_at"] = datetime.strptime(updated, time_format)

            # Apply provided attributes
            self.__dict__.update(kwargs)

            # Ensure required attributes exist even if missing from kwargs
            if "id" not in self.__dict__:
                self.id = str(uuid4())
            if "created_at" not in self.__dict__:
                self.created_at = datetime.now()
            if "updated_at" not in self.__dict__:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def save(self):
        """Update `updated_at` and persist via storage."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Return a dictionary containing a simple-typed representation.

        Datetime fields are ISO-formatted strings and `__class__` is included
        with the class name of the object.
        """
        data = self.__dict__.copy()
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        data["__class__"] = self.__class__.__name__
        return data

    def __str__(self):
        """Return the canonical string representation."""
        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)
