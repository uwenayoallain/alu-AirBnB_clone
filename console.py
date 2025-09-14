#!/usr/bin/python3
"""Defines AirBnb console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __all_classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """
        Called when an empty line is entered.
        If this method is not overridden like this,
        it repeats the last nonempty
        command entered.
        It should not be empty_line, so ignore the typo warnings.
        (see: https://github.com/python/cpython/blob/3.11/Lib/cmd.py)
        """
        pass

    def default(self, arg):
        """This is the default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command -> exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal -> exit the program."""
        print("")
        return True

    def do_create(self, args):
        """
            Creates a new instance of a class,
            saves it (to the JSON file) and prints the id.
            Usage: create <class_name>
       """
        # If the class name is missing,
        # print ** class name missing ** (ex: $ create)
        if len(args) < 1:
            print("** class name missing **")
            return
        # If the class name doesn’t exist,
        # print ** class doesn't exist ** (ex: $ create MyModel)

        # convert the args to a list
        args = args.split()

        # the 1st element of the list is the class name
        class_name = args[0]
        if class_name not in self.__all_classes:
            print("** class doesn't exist **")
            return
        # print(self.__all_classes)
        # eval() interprets a string as a piece of python code
        new_object = eval(class_name + "()")
        new_object.save()
        print(new_object.id)
        storage.save()

    def do_show(self, args):
        """Usage: to show <class> <id> or <class>.show(<id>)
        Display string representation of a class instance of given id.
        """
        arg_list = args.split()
        objdict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
            return
        elif arg_list[0] not in self.__all_classes:
            print("** class doesn't exist **")
            return
        elif len(arg_list) == 1:
            print("** instance id missing **")
            return

        object_key = "{}.{}".format(arg_list[0], arg_list[1])

        if object_key not in objdict:
            print("** no instance found **")
            return
        else:
            print(objdict[object_key])

    def do_destroy(self, args):
        """Usage: to destroy <class> <id> or <class>.destroy(<id>)
        Delete class instance of given id."""

        arg_list = args.split()
        all_objects = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
            return
        class_name = arg_list[0]
        if class_name not in self.__all_classes:
            print("** class doesn't exist **")
            return
        if len(arg_list) == 1:
            print("** instance id missing **")
            return
        instance_id = arg_list[1]

        object_key = "{}.{}".format(class_name, instance_id)

        if object_key not in all_objects.keys():
            print("** no instance found **")
        else:
            del all_objects[object_key]
            storage.save()

    def do_all(self, args):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of given class
        If no class is specified, display all instantiated objects."""

        arg_list = args.split()
        all_objects = storage.all()
        object_list = []
        if len(arg_list) == 0:
            for obj in all_objects.values():
                object_list.append(obj.__str__())
            print(list(object_list))
            return

        if len(arg_list) > 0 and arg_list[0] not in self.__all_classes:
            print("** class doesn't exist **")
            return
        class_name = arg_list[0]
        object_list = []

        for obj in all_objects:
            if class_name == all_objects[obj].__class__.__name__:
                object_list.append(str(all_objects[obj]))
        print(object_list)

    def do_count(self, args):
        """Usage: to count <class> or <class>.count()
        Retrieve number of instances of given class."""

        arg_list = args.split()
        count = 0
        for obj in storage.all().values():
            if arg_list[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, args):
        """Usage:
        - update <class> <id> <attribute_name> "<attribute_value>"
        - <class>.update(<id>, <attribute_name>, <attribute_value>)
        - <class>.update(<id>, <dictionary>)

        Updates a class instance of the given id by adding or updating
        one attribute, or many when a dictionary is provided. Values are
        cast to the attribute's type when the attribute exists on the class.
        """

        tokens = parse(args)
        objects = storage.all()

        if len(tokens) == 0:
            print("** class name missing **")
            return False

        class_name = tokens[0]
        if class_name not in self.__all_classes:
            print("** class doesn't exist **")
            return False

        if len(tokens) == 1:
            print("** instance id missing **")
            return False

        instance_id = tokens[1]
        key = f"{class_name}.{instance_id}"
        if key not in objects:
            print("** no instance found **")
            return False

        obj = objects[key]

        # Dictionary update form
        if len(tokens) == 3:
            try:
                payload = eval(tokens[2])
            except Exception:
                payload = None
            if isinstance(payload, dict):
                for k, v in payload.items():
                    # Skip core fields if provided accidentally
                    if k in {"id", "created_at", "updated_at"}:
                        continue
                    self._set_attr_with_cast(obj, k, v)
                obj.save()
                return
            else:
                print("** attribute name missing **")
                return False

        if len(tokens) == 2:
            print("** attribute name missing **")
            return False

        if len(tokens) == 3:
            print("** value missing **")
            return False

        attr_name = tokens[2]
        if len(tokens) < 4:
            print("** value missing **")
            return False
        raw_val = tokens[3]

        # Skip core fields
        if attr_name in {"id", "created_at", "updated_at"}:
            return False

        self._set_attr_with_cast(obj, attr_name, raw_val)
        obj.save()

    def _set_attr_with_cast(self, obj, name, value):
        """Helper to set attribute on obj, casting to class attribute type
        when defined (supports str, int, float)."""
        # If coming from parsed tokens, strings are already unquoted
        target_type = None
        if hasattr(obj.__class__, name):
            target_type = type(getattr(obj.__class__, name))
        elif hasattr(obj, name):
            current = getattr(obj, name)
            target_type = type(current)

        casted = value
        if target_type in {int, float, str}:
            try:
                casted = target_type(value)
            except Exception:
                # Fallback: attempt numeric inference when class type not known
                casted = value
        else:
            # Try to interpret numeric values when no target type is known
            if isinstance(value, str):
                try:
                    if "." in value:
                        casted = float(value)
                    else:
                        casted = int(value)
                except Exception:
                    casted = value

        setattr(obj, name, casted)


if __name__ == "__main__":
    """
    Repeatedly issue a prompt, accept input, parse an initial prefix
    off the received input, and dispatch to action methods, passing them
    the remainder of the line as argument.
    (see: https://github.com/python/cpython/blob/3.8/Lib/cmd.py#L98)
    """
    HBNBCommand().cmdloop()
