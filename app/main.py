import argparse
import os
import shutil
import time
from datetime import datetime


def get_args() -> tuple:
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--source-path',
                        help='Path of the source folder')
    parser.add_argument('-r', '--replica-path',
                        help='Path of the replica folder')
    parser.add_argument('-i', '--synch-interval',
                        help='Synchronization interval in seconds. Default: 3600 (1 hour)', default='3600')
    parser.add_argument('-l', '--log-path',
                        help='Path of the log file. Default: current path with name log_file.txt', default='log_file.txt')

    args = parser.parse_args()

    if args.source_path == None:
        raise OSError('Missing source path!')
    if args.replica_path == None:
        raise OSError('Missing replica path!')
    if not args.synch_interval.isnumeric():
        raise OSError('Synchcronization interval needs to be an integer!')

    return args.source_path, args.replica_path, int(args.synch_interval), args.log_path


def get_dir_list(path: str = '.', aux: str = '') -> list:
    # a parent is always on the left, that is, an object only appears after its folder
    objects = []
    for object in os.listdir(path):
        full_path = os.path.join(path, object)
        if os.path.isdir(full_path):
            objects.append(aux + object if aux else object)
            objects += get_dir_list(full_path, aux + object + '\\')
        else:
            objects.append(aux + object if aux else object)
    return objects


def get_combined_dir(source_path: str, replica_path: list):

    source_list = get_dir_list(source_path)
    replica_list = get_dir_list(replica_path)
    replica_list.reverse()
    # replica is reversed because items there are to be deleted, so the folders must be to the right of files
    return source_list + [o for o in replica_list if o not in source_list]


def update_folder(source: str, replica: str, logs: list) -> None:

    if not os.path.exists(replica):
        os.makedirs(replica)
        log = f'{datetime.now()} - Created folder {replica}'
        logs.append(log)
        print(log)

    elif not os.path.exists(source):
        os.rmdir(replica)
        log = f'{datetime.now()} - Deleted folder {replica}'
        logs.append(log)
        print(log)


def update_file_modifications(source: str, replica: str, logs: list) -> None:

    if not os.path.exists(source):
        os.remove(replica)
        log = f'{datetime.now()} - Deleted file {replica}'
        logs.append(log)
        print(log)

    elif not os.path.exists(replica):
        shutil.copy(source, replica)
        log = f'{datetime.now()} - Created file {replica}'
        logs.append(log)
        print(log)

    elif os.path.getmtime(replica) < os.path.getmtime(source):
        shutil.copy(source, replica)
        log = f'{datetime.now()} - Updated file {replica}'
        logs.append(log)
        print(log)


def is_folder(source, replica):
    return os.path.isdir(source) if os.path.exists(source) else os.path.isdir(replica)


def update(source: str, replica: str, logs: list):
    if is_folder(source, replica):
        update_folder(source, replica, logs)
    else:
        update_file_modifications(source, replica, logs)


def is_from_source(source_path):
    return 'source' if os.path.exists(source_path) else 'replica'


def main():

    source, replica, synch_interval, log_path = get_args()

    while True:
        dir_list = get_combined_dir(source, replica)
        logs = []

        for object in dir_list:
            source_path = os.path.join(source, object)
            replica_path = os.path.join(replica, object)
            update(source_path, replica_path, logs)

        with open(log_path, 'a') as f:
            for log in logs:
                f.write(log + '\n')
            f.write('\n') if logs else None

        time.sleep(synch_interval)

if __name__ == '__main__':
    main()
