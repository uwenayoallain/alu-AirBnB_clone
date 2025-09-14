# AirBnB Clone - The Console

Simple command-line interpreter for managing objects for the AirBnB clone project. This is the first step of a larger web application that will later include storage backends, a REST API, and a web front end.

## Project Overview
- Parent class `BaseModel` handling initialization, serialization and deserialization
- Simple flow: Instance <-> Dictionary <-> JSON string <-> file
- Storage engine abstraction (file storage for now)
- First set of models inheriting from `BaseModel` (e.g., `User`, `State`, `City`, `Place`, `Amenity`, `Review`)
- Unittests to validate models and storage engine

## Requirements
- Python 3.8.5
- Ubuntu 20.04 LTS
- pycodestyle 2.7.*

## Repository Structure (partial)
- `console.py` — entry point for the command interpreter
- `models/` — package with `BaseModel` and other models
- `models/engine/file_storage.py` — file-based storage engine
- `tests/` — unittests

## How To Start the Console
Interactive mode:

```
./console.py
(hbnb) help
```

Non-interactive mode:

```
echo "help" | ./console.py
```

Ensure the file is executable if needed:

```
chmod +x console.py
```

## How To Use the Console
General syntax uses the `cmd` module style:

- `create <ClassName>` — create a new instance, persist to storage, print its id
- `show <ClassName> <id>` — print the string representation of an instance
- `destroy <ClassName> <id>` — delete an instance and save
- `all [<ClassName>]` — print all instances, optionally filtered by class
- `update <ClassName> <id> <attribute_name> "<attribute_value>"` — update one attribute and save
- `count <ClassName>` — count instances of a class
- `quit` or `EOF` — exit the interpreter

Arguments are space-separated; strings with spaces must be wrapped in double quotes.

Also supported are object-oriented style calls, e.g. `<ClassName>.all()`, `<ClassName>.show(<id>)`, `<ClassName>.destroy(<id>)`, `<ClassName>.count()`, `<ClassName>.update(<id>, <attr>, <value>)` or `<ClassName>.update(<id>, <dict>)` when applicable.

## Examples
Interactive session:

```
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb) create BaseModel
49faff9a-6318-451f-87b6-910505c55907
(hbnb) show BaseModel 49faff9a-6318-451f-87b6-910505c55907
[BaseModel] (49faff9a-6318-451f-87b6-910505c55907) { ... }
(hbnb) all BaseModel
["[BaseModel] (49faff9a-6318-451f-87b6-910505c55907) {...}"]
(hbnb) update BaseModel 49faff9a-6318-451f-87b6-910505c55907 first_name "Betty"
(hbnb) show BaseModel 49faff9a-6318-451f-87b6-910505c55907
[BaseModel] (49faff9a-6318-451f-87b6-910505c55907) { 'first_name': 'Betty', ... }
(hbnb) quit
```

Non-interactive run of tests:

```
echo "python3 -m unittest discover tests" | bash
```

## Running Tests
From the project root, run all tests:

```
python3 -m unittest discover tests
```

Run a specific test file:

```
python3 -m unittest tests/test_models/test_base_model.py
```

## Authors
See `AUTHORS` for the list of contributors.
