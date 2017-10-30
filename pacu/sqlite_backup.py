import os
import shutil
import datetime

data_root = '/home/pacu/.pacu/scanbox'
backup_root = '/mnt/data/Recordings/scanbox-data'

def create_backups():
    date = datetime.datetime.now().date()
    backup_location = date.isoformat()
    for root, _, files in os.walk(data_root):
        if any(['sqlite3' in f for f in files]):
            file_root = re.sub(data_root + '/', '', root)
            path = os.path.join(backup_root, backup_location, file_root)
            os.makedirs(path, exist_ok=True)
            shutil.copy(os.path.join(root, 'db.sqlite3'), path)
