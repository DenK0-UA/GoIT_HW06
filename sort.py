import os
import re
import shutil
import sys
import zipfile


def normalize(name):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g',
        'д': 'd', 'е': 'e', 'є': 'ye', 'ж': 'zh', 'з': 'z',
        'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': '', 'ю': 'iu', 'я': 'ia', 'А': 'A', 'Б': 'B',
        'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E',
        'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z', 'И': 'Y', 'І': 'I',
        'Ї': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S',
        'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts',
        'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ь': '', 'Ю': 'Iu',
        'Я': 'Ya'
    }

    translation_table = str.maketrans(translit_dict)
    name = name.translate(translation_table)
    name = re.sub(r'[^A-Za-z0-9.]+', '_', name)

    return name


def move_files(source, destination):
    for root, dirs, files in os.walk(source):
        for file in files:
            file_path = os.path.join(root, file)
            destination_path = os.path.join(destination, file)
            shutil.move(file_path, destination_path)


def remove_empty_folders(folder):
    for root, dirs, files in os.walk(folder, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


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
                        if os.path.exists(new_item_path):
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
                if os.path.exists(new_item_path):
                    continue

                os.rename(item_path, new_item_path)

    return files_by_type, unknown_extensions


def organize_files(files, destination_path):
    for category, file_list in files.items():
        category_path = os.path.join(destination_path, category)
        os.makedirs(category_path, exist_ok=True)

        for file in file_list:
            file_path = os.path.join(destination_path, file)

            if category == 'archives':
                archive_name = os.path.splitext(file)[0]
                archive_path = os.path.join(category_path, archive_name)
                os.makedirs(archive_path, exist_ok=True)

                if zipfile.is_zipfile(file_path):
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(archive_path)
                    os.remove(file_path)
                else:
                    print(f"Unsupported archive format: {file}")

            else:
                new_file_path = os.path.join(category_path, file)
                shutil.move(file_path, new_file_path)


def main():
    folder_path = sys.argv[1]
    destination_path = folder_path
    files, unknown_extensions = scan_folder(folder_path)

    move_files(folder_path, destination_path)
    remove_empty_folders(folder_path)
    organize_files(files, destination_path)

    print("List of files by type:")
    for category, file_list in files.items():
        print(f"{category}: {', '.join(file_list)}")

    print("Unknown extensions:")
    print(', '.join(unknown_extensions))


if __name__ == "__main__":
    main()
