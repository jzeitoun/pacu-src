import datetime
import schedule
import logging
import daemon
import os
import sys
import shutil
import time
import re

from setproctitle import setproctitle

data_root = '/home/pacu/.pacu/scanbox'
backup_root = '/mnt/data/Recordings/scanbox-data/pacu-backups'
log_file = 'sqlite_backup.log'

'''

Creates daily backup of pacu data.

'''

def exception_handler(type, value, tb):
    logger.exception('Uncaught exception: {0}'.format(str(value)))

def create_backups(logger):
    date = datetime.datetime.now().date()
    backup_location = date.isoformat()
    for root, _, files in os.walk(data_root):
        if any(['sqlite3' in f for f in files]):
            file_root = re.sub(data_root + '/', '', root)
            path = os.path.join(backup_root, backup_location, file_root)
            try:
                os.makedirs(path)
                shutil.copy(os.path.join(root, 'db.sqlite3'), path)
            except Exception as e:
                logger.error(e)
                logger.error('Skipping: {}'.format(root))

def run_daemon():
    logger = logging.getLogger(__name__)
    log_path = os.path.join(backup_root, log_file)

    if not os.path.exists(log_path):
        open(log_path, 'w')

    logging.basicConfig(
        filename=log_path,
        format='%(asctime)s %(message)s',
        level=logging.DEBUG,
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )

    # install exception handler
    sys.excepthook = exception_handler

    # schedule backup at 8:00 AM daily
    schedule.every().day.at("8:00").do(create_backups, logger)

    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    with daemon.DaemonContext():
        run_daemon()

if __name__ == '__main__':
    setproctitle('pacu-backupd')
    main()
