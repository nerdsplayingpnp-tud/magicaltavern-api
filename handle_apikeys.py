import os
from pathlib import Path


def _ensurepaths() -> None:
    Path("data/keys.txt").touch(exist_ok=True)


def validate(key: str) -> bool:
    _ensurepaths()
    return "a"
