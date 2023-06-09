import os
import json
import sqlite3

# Set up the SQLite database
conn = sqlite3.connect('amm.db')
c = conn.cursor()

# Reset sqlite table
c.execute('DROP TABLE IF EXISTS repos')
c.execute('DROP TABLE IF EXISTS checkpoints')
c.execute('DROP TABLE IF EXISTS file_records')

# Create the table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS repos
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              registry TEXT,
              registryId TEXT,
              subtype TEXT,
              latestDownload INT,
              name TEXT,
              data TEXT
              )
              ''')

# Create checkpoint table
c.execute('''CREATE TABLE IF NOT EXISTS checkpoints
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repoId TEXT,
    data TEXT
)
''')

# Create file records table
c.execute('''CREATE TABLE IF NOT EXISTS file_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    checkpointId TEXT,
    filename TEXT,
    url TEXT,
    data TEXT
    )
''')

# handle civitai
dir_path = 'civitai/model-indices'
for filename in os.listdir(dir_path):
    if filename.endswith('.json'):
        with open(os.path.join(dir_path, filename), 'r') as f:
            data = json.load(f)
            for item in data["items"]:
                c.execute(
                    '''
                    INSERT INTO repos (
                        registry,
                        registryId,
                        subtype,
                        latestDownload,
                        name,
                        data
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        "civitai",
                        str(item["id"]),
                        item["type"],
                        item["stats"]["downloadCount"],
                        item["name"],
                        json.dumps(item)
                    )
                )
                checkpoints = item["modelVersions"]
                for checkpoint in checkpoints:
                    c.execute(
                        '''
                        INSERT INTO checkpoints (
                            repoId,
                            data
                        ) VALUES (?, ?)
                        ''',
                        (
                            c.lastrowid,
                            json.dumps(checkpoint)
                        )
                    )

                    checkpointId = c.lastrowid
                    files = checkpoint["files"]
                    for file in files:
                        c.execute(
                            '''
                            INSERT INTO file_records (
                                checkpointId,
                                filename,
                                url
                            ) VALUES (?, ?, ?)
                            ''',
                            (
                                checkpointId,
                                file["name"],
                                file["downloadUrl"]
                            )
                        )

                conn.commit()

# handle huggingface
dir_path = 'huggingface/model-indices'
for filename in os.listdir(dir_path):
    if filename.endswith('.json'):
        with open(os.path.join(dir_path, filename), 'r') as f:
            data = json.load(f)
            for item in data:
                c.execute(
                    '''
                    INSERT INTO repos (
                        registry,
                        registryId,
                        subtype,
                        latestDownload,
                        name,
                        data
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        "huggingface",
                        str(item["id"]),
                        item.get("pipeline_tag", ""),
                        item["downloads"],
                        item["id"],
                        json.dumps(item)
                    )
                )
                c.execute(
                    '''
                    INSERT INTO checkpoints (
                        repoId,
                        data
                    ) VALUES (?, ?)
                    ''',
                    (
                        c.lastrowid,
                        json.dumps({
                            "sha": item["sha"],
                        })
                    )
                )
                checkpoint_id = c.lastrowid

                files = item.get("siblings", [])
                for file in files:
                    c.execute(
                        '''
                        INSERT INTO file_records (
                            checkpointId,
                            filename,
                            url
                        ) VALUES (?, ?, ?)
                        ''',
                        (
                            checkpoint_id,
                            file["rfilename"],
                            # like this: https://huggingface.co/nitrosocke/Nitro-Diffusion/resolve/70e3387b971acebcc9ecd0f93e2ff5cdb9308b5c/nitroDiffusion-v1.ckpt
                            "https://huggingface.co/{}/resolve/{}/{}".format(item['modelId'], item["sha"],
                                                                             file["rfilename"])
                        )
                    )

                conn.commit()

# Close the SQLite connection
conn.close()
