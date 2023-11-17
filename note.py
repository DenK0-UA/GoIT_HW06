import os
import re
import shutil
import sys
import zipfile

def scan_folder(folder_path):
    file_types = {
        'images': ['jpeg', 'png', 'jpg', 'svg', 'bmp'],
        'videos': ['avi', 'mp4', 'mov', 'mkv'],
        'documents': ['doc', 'docx', 'txt', 'pdf', 'xls', 'xlsx', 'pptx'],
        'music': ['mp3', 'ogg', 'wav', 'amr'],
        'archives': ['zip', 'gz', 'tar']
    }

    files_by_type = {category: [] for category in file_types}
    unknown_extensions = []

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            extension = item.split('.')[-1]
            added_to_category = False

            for category, extensions in file_types.items():
                if extension in extensions:
                    normalized_name = normalize(item.split('.')[0]) + '.' + extension
                    new_item_path = os.path.join(folder_path, normalized_name)

                    if item_path.lower() != new_item_path.lower():
                        # Check if a file with the same name already exists
                        if os.path.exists(new_item_path):
                            # Handle the conflict by skipping the renaming process
                            added_to_category = True
                            break

                        os.rename(item_path, new_item_path)

                    files_by_type[category].append(normalized_name)
                    added_to_category = True
                    break

            if not added_to_category:
                unknown_extensions.append(item)

        elif os.path.isdir(item_path):
            subfolder_files, subfolder_unknown = scan_folder(item_path)

            for category, files in subfolder_files.items():
                files_by_type[category].extend(files)

            unknown_extensions.extend(subfolder_unknown)

            normalized_name = normalize(item)
            new_item_path = os.path.join(folder_path, normalized_name)

            if item_path.lower() != new_item_path.lower():
                # Check if a folder with the same name already exists
                if os.path.exists(new_item_path):
                    # Handle the conflict by skipping the renaming process
                    continue

                os.rename(item_path, new_item_path)

    return files_by_type, unknown_extensions