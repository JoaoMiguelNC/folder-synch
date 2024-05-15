# Folder Synchronization

Given a source and a replica folder, assuming that the files in replica are not manually altered, the code will synch the files of the replica folder to match the content of the source folder.

The logs are printed to the console and to a log file.

The program takes four arguments:
- `-s`, `--source-path` Path of the source folder
- `-r`, `--replica-path` Path of the replica folder
- `-i`, `--synch-interval` Synchronization interval in seconds. Default: 3600 (1 hour)
- `-s`, `--source-path` Path of the log file. Default: current path with name log_file.txt

