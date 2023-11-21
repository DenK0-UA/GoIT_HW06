import os


def remove_empty_folders(folder):
    for root, dirs, files in os.walk(folder, topdown=False):
        for i in dirs:
            dir_path = os.path.join(root, i)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
