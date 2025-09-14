#!/usr/bin/python3
""" Known classes """

from ..base_model import BaseModel
from ..amenity import Amenity
from ..city import City
from ..place import Place
from ..review import Review
from ..state import State
from ..user import User

classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}

console_methods = ["all", "count", "show", "destroy", "update"]