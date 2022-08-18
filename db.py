import json
from pathlib import Path


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
        self.file = file
        # We are using self-made memory caching! Hopefully it makes sense...
        self.cache_valid: bool = False
        self.cache: dict = {}

    def _validate_cache(self):
        # If the cache isn't valid anymore: Revalidate it by acquiring the data from disk.
        if not self.cache_valid:
            with open(self.file, mode="r", encoding="utf8") as database_file:
                self.cache = json.load(database_file)
                database_file.close()
                self.cache_valid = True

    def get_key(self, key: int) -> any:
        # Key needs to be a string
        key = str(key)
        # If the cache is valid: Return the cached value that belongs to the key.
        # If it is not valid: Re-validate cache and then get the value that belongs to the key.
        self._validate_cache()
        return self.cache.get(key)

    def set_key(self, data: any, key: int = None) -> bool:
        self._validate_cache()
        # If no key attribute has been given, use auto-incrementing values.
        if key == None:
            key = len(self.cache.keys()) + 1
        # Key needs to be a string
        key = str(key)
        # Put the data where it belongs. Either as a new entry, or by updating an existing entry.
        self.cache.update({key: data})
        with open(self.file, mode="w", encoding="utf8") as database_file:
            # Write changes to disk.
            json.dump(self.cache, database_file)
        # Invalidate cache, just to be sure that the cached information is always correct.
        # TODO: Check, if this is even necessary. The cache also gets updated in line 61, so
        # we should not have to do this.
        self.cache_valid = False
        return True
