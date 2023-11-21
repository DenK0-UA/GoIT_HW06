import os
from normalize import normalize


def scan_folder(folder_path):
    file_types = {
        'images': ['jpeg', 'png', 'jpg', 'svg', 'bmp', 'JPEG', 'PNG', 'JPG', 'SVG', 'BMP'],
        'video': ['avi', 'mp4', 'mov', 'mkv', 'AVI', 'MP4', 'MOV', 'MKV'],
        'documents': ['doc', 'docx', 'txt', 'pdf', 'xls', 'xlsx', 'pptx', 'DOC', 'DOCX', 'TXT', 'PDF', 'XLS', 'XLSX',
                      'PPTX'],
        'audio': ['mp3', 'ogg', 'wav', 'amr', 'MP3', 'OGG', 'WAV', 'AMR'],
        'archives': ['zip', 'gz', 'tar', 'rar', 'ZIP', 'GZ', 'TAR', 'RAR']
    }

    files_by_type = {category: [] for category in file_types}
    unknown_extensions = []

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            extension = item.split('.')[-1]
            added_to_category = False

            for category, extensions in file_types.items():
                if extension.lower() in extensions:
                    normalized_name = normalize(item.split('.')[0]) + '.' + extension
                    new_item_path = os.path.join(folder_path, normalized_name)

                    if item_path != new_item_path:
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

            if item_path != new_item_path:
                if os.path.exists(new_item_path):
                    continue

                os.rename(item_path, new_item_path)

    return files_by_type, unknown_extensions
