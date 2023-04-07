import sys
import os
import json
from typing import List, TypedDict


class DependencyItem(TypedDict):
    name: str
    url: str
    version: str


class Config(TypedDict):
    amm_version: str
    name: str
    root: str
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


def main() -> None:
    verb = sys.argv[1]
    if verb == "init":
        init(sys.argv[2:])
    else:
        print("Unknown verb", verb)


main()
