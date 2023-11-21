import os
import shutil


def move_unknown_files(unknown_files, destination_path):
    unknown_files_path = os.path.join(destination_path, 'unknown_files')
    os.makedirs(unknown_files_path, exist_ok=True)

    for file in unknown_files:
        file_path = os.path.join(destination_path, file)
        new_file_path = os.path.join(unknown_files_path, file)
        shutil.move(file_path, new_file_path)
