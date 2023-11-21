import os
import shutil
import zipfile


def organize_files(files, destination_path):
    for category, file_list in files.items():
        if category == 'archives':
            category_path = os.path.join(destination_path, category)
            os.makedirs(category_path, exist_ok=True)

            for file in file_list:
                file_path = os.path.join(destination_path, file)
                archive_name = os.path.splitext(file)[0]
                archive_path = os.path.join(category_path, archive_name)
                os.makedirs(archive_path, exist_ok=True)

                if zipfile.is_zipfile(file_path):
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(archive_path)
                    os.remove(file_path)
                else:
                    print(f"Unsupported archive format: {file}")

        elif category in ['video', 'audio', 'documents', 'images']:
            category_path = os.path.join(destination_path, category)
            os.makedirs(category_path, exist_ok=True)

            for file in file_list:
                file_path = os.path.join(destination_path, file)
                new_file_path = os.path.join(category_path, file)
                shutil.move(file_path, new_file_path)

        else:
            print(f"Unknown category: {category}")
