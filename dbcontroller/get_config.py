from pathlib import Path
from json import load


def get_config() -> dict:
    with open(Path('dbcontroller', 'config.json')) as f:
        return load(f)
