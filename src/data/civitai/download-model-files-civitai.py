# load data from sqlite3
import os
import sqlite3
from b2_amm import upload_amm
import subprocess

def main():
    conn = sqlite3.connect("./amm.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
    SELECT id, registryId, name FROM repos
    WHERE registry = "civitai"
    ORDER BY latestDownload DESC
    LIMIT 1000
    ''')
    rows = c.fetchall()
    root = "download-all-civitai"
    for row in rows:
        # get checkpoints matching the repo
        c.execute('SELECT id, repoId FROM checkpoints WHERE repoId = ?', (row['id'],))
        checkpoints = c.fetchall()
        for checkpoint in checkpoints:
            # get file records matching the checkpoint
            c.execute('SELECT filename, url FROM file_records WHERE checkpointId = ?', (checkpoint['id'],))
            file_records = c.fetchall()
            for file_record in file_records:
                # download the file
                local_root = os.path.join(root, row['name'])
                if not os.path.exists(local_root):
                    os.makedirs(local_root, exist_ok=True)
                filename = file_record['filename']
                url = file_record['url']
                final_path = os.path.join(local_root, filename)
                print("downloading", local_root, filename, url)
                # check if file already exists, if so, skip it
                print('executing wget --content-disposition -O "{}" {}'.format(final_path, url))
                os.system('wget --content-disposition -O "{}" {}'.format(final_path, url))
                print(f"\nwget done; starting upload {final_path}\n")
                upload_amm(final_path, filename)
                print("\nupload finished\n")
                os.remove(final_path)

if __name__ == "__main__":
    main()
