import json
import random
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
dbsql = SQLAlchemy()

def make_file(file: str) -> Path:
    """Create a file (and its' path), if it doesn't already exist.

    Args:
        file (str): Path to file

    Returns:
        Path: Path object
    """
    # From the String "file", cut off everything before the name of the file (so that you have)
    # a directory. The part we want is EVERYTHING BEFORE the last '/'),
    # check if this directory exists, and if it doesn't: create it!
    Path(file[0 : file.rfind("/")]).mkdir(parents=True, exist_ok=True)
    # Then proceed to create the file in the directory.
    file_path = Path(file)
    if not file_path.is_file():
        file_path.touch(exist_ok=True)
        with open(file_path, mode="w", encoding="utf8") as init_file:
            # Initialize the json file with curly brackets, so that it can be worked with.
            json.dump({}, init_file)
            init_file.close()

    return file_path


class Database:
    def __init__(self, file: Path) -> None:
        """A Database object represents a (unique), cached connection to a database file.

        Args:
            file (Path): a pathlib.Path to the database file. Must be a .json file.
        """
        self.file = file
        # We are using self-made memory caching! Hopefully it makes sense...
        self.__cache_valid: bool = False
        self.__cache: dict = {}

    def __validate_cache(self):
        # If the cache isn't valid anymore: Revalidate it by acquiring the data from disk.
        if not self.__cache_valid:
            with open(self.file, mode="r", encoding="utf8") as database_file:
                self.__cache = json.load(database_file)
                database_file.close()
                self.__cache_valid = True

    def get_key(self, key: int) -> any:
        """Gets the value of the given key in the database file, if the key exists.

        Args:
            key (int): The key, whose value should be returned.

        Returns:
            any: The value assigned to the key.
        """
        # Key needs to be a string
        key = str(key)
        # If the cache is valid: Return the cached value that belongs to the key.
        # If it is not valid: Re-validate cache and then get the value that belongs to the key.
        self.__validate_cache()
        return self.__cache.get(key)

    def get_all(self) -> dict:
        """Get all the key: value pairs from the database file.

        Returns:
            any: key: value pairs from the database file.
        """
        # If the cache is valid: Return the cached value that belongs to the key.
        # If it is not valid: Re-validate cache and then get the value that belongs to the key.
        self.__validate_cache()
        return self.__cache

    def set_key(self, data: any, key: int = None) -> str:
        """Add a new key: value pair to the database file, if the 'key' parameter is either left empty
        or if the 'key' parameter doesn't exist in the database yet. Update an existing key: value
        pair in the database, if the specified 'key' parameter already exists. If the 'key'
        parameter is left empty, a 'random' 6-digit-number that does not already exist in the
        database will be used as a key.
        Args:
            data (any): Any data that can be stored as a json value.
            key (int, optional): Optional key parameter. Defaults to None.

        Returns:
            str: id of the created resource in the database.
        """
        self.__validate_cache()
        # If no key attribute has been given, use auto-incrementing values.
        if key is None:
            random.seed()
            while True:
                key = str(random.randint(0, 9))
                for i in range(5):
                    key = key + str(random.randint(0, 9))
                if key not in self.__cache.keys():
                    break
        # Key needs to be a string. Typecast is necessary, if key is given as function parameter.
        key = str(key)
        # Put the data where it belongs. Either as a new entry, or by updating an existing entry.
        db = self.__cache
        db.update({key: data})
        with open(self.file, mode="w", encoding="utf8") as database_file:
            # Write changes to disk.
            json.dump(db, database_file, indent=4)
        # Invalidate cache, since the data on the disk has changed.
        self.__cache_valid = False
        return key

    def has_key(self, key: int) -> bool:
        """Checks, if a key is present in the database file.

        Args:
            key (int): The key to be checked.

        Returns:
            bool: True, if the key exists. False, if the key does not exist.
        """
        key = str(key)
        self.__validate_cache()
        keys = self.__cache.keys()
        if key in keys:
            return True
        return False
