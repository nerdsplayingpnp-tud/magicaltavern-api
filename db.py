import json
from pathlib import Path


def make_file(file: str) -> Path:
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

    return Path(file)


class Database:
    def __init__(self, file: Path) -> None:
        self.file = file
        self.cache_valid: bool = False
        self.cache: dict = {}

    def _validate_cache(self):
        if not self.cache_valid:
            with open(self.file, mode="r", encoding="utf8") as database_file:
                self.cache = json.load(database_file)
                database_file.close()
                self.cache_valid = True

    def get_key(self, key: int) -> any:
        self._validate_cache()
        return self.cache.get(key)

    def set_key(self, key: int, data: any) -> bool:
        self._validate_cache()
        self.cache.update({key: data})
        with open(self.file, mode="w", encoding="utf8") as database_file:
            json.dump(self.cache, database_file)
        self.cache_valid = False
        return True
