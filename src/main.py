import sys
import os
import json
from typing import List, TypedDict, Tuple


class DependencyItem(TypedDict):
    name: str
    url: str
    version: str
    root: str


class Config(TypedDict):
    amm_version: str
    name: str
    items: List[DependencyItem]


CONFIG_FILE = "amm.json"


def init(args: List[str]) -> None:
    config = Config(
        amm_version='0.1.0',
        name="Something",
        root=".",
        items=[],
    )

    json_text = json.dumps(config, indent=4)
    if os.path.isfile(CONFIG_FILE):
        print("{} exists. skipping...".format(CONFIG_FILE))
    else:
        with open(CONFIG_FILE, 'w') as file:
            file.write(json_text)
            print("{} saved".format(CONFIG_FILE))
            print(json_text)


MODEL_SUFFICES = [
    "safetensors",
    "ckpt",
    "bin",
    "pth",
]

def is_model(name: str) -> bool:
    for suffix in MODEL_SUFFICES:
        if name.endswith(suffix):
            return True
    return False


def probe(args: List[str]) -> None:
    model_paths: List[str] = []
    for (base, subdirectories, filenames) in os.walk("."):
        for name in filenames:
            if is_model(name):
                model_paths.append(os.path.join(base, name))

    print(model_paths)


def main() -> None:
    verb = sys.argv[1]
    if verb == "init":
        init(sys.argv[2:])
    elif verb == "probe":
        probe(sys.argv[2:])
    else:
        print("Unknown verb", verb)


main()
