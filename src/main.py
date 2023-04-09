import sys
import os
import json
import sqlite3
from typing import List, TypedDict, Tuple


class DependencyItem(TypedDict):
    name: str
    url: str
    version: str
    root: str


class ModuleConfig(TypedDict):
    amm_version: str
    name: str
    items: List[DependencyItem]

CONFIG_FILE = "amm.json"

DB_FILE = 'src/data/amm.db'


def init(args: List[str]) -> None:
    config = ModuleConfig(
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
    search_root = "."
    if len(args) >= 1:
        search_root = args[0]

    db_file = DB_FILE
    if len(args) >= 2:
        db_file = args[1]

    model_paths: List[(str, str)] = []
    for (base, subdirectories, filenames) in os.walk(search_root):
        for name in filenames:
            if is_model(name):
                model_paths.append((base, name))

    dependencies: List[DependencyItem] = []

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    for (base, name) in model_paths:
        print("\nfitting file {}".format(name))
        c.execute("""
        SELECT repos.id, repos.registry, repos.name, repos.latestDownload, file_records.url FROM file_records
        JOIN checkpoints ON file_records.checkpointId = checkpoints.id
        JOIN repos ON repos.id = checkpoints.repoId
        WHERE file_records.filename LIKE '%{}%'
        ORDER BY repos.latestDownload DESC;
        """.format(name))
        # print select result
        rows = c.fetchall()
        # TODO: handle multiple results
        relative_path = os.path.relpath(base, search_root)
        if len(rows) >= 1:
            row = rows[0]
            dependencies.append({
                "name": name,
                "url": row["url"],
                "version": "",
                "root": relative_path,
            })
            print("best match: {}".format(row["url"]))
        else:
            dependencies.append({
                "name": name,
                "url": "",
                "version": "",
                "root": relative_path,
            })

    config = ModuleConfig(
        amm_version='0.1.0',
        name="Something",
        root=".",
        items=dependencies,
    )

    # save config to json
    json_text = json.dumps(config, indent=4)
    with open(CONFIG_FILE, 'w') as file:
        file.write(json_text)
        print("{} saved".format(CONFIG_FILE))
        print(json_text)



def main() -> None:
    verb = sys.argv[1]
    if verb == "init":
        init(sys.argv[2:])
    elif verb == "probe":
        probe(sys.argv[2:])
    else:
        print("Unknown verb", verb)


main()
