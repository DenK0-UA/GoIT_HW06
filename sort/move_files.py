import os
import shutil


def move_files(source, destination):
    for root, dirs, files in os.walk(source):
        for file in files:
            file_path = os.path.join(root, file)
            destination_path = os.path.join(destination, file)
            shutil.move(file_path, destination_path)
