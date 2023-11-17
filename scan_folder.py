import os
import normalize


def scan_folder(folder_path):
    # Словник, що містить розширення файлів для кожної категорії
    file_types = {
        'images': ['jpeg', 'png', 'jpg', 'svg', 'bmp'],
        'videos': ['avi', 'mp4', 'mov', 'mkv'],
        'documents': ['doc', 'docx', 'txt', 'pdf', 'xls', 'xlsx', 'pptx'],
        'music': ['mp3', 'ogg', 'wav', 'amr'],
        'archives': ['zip', 'gz', 'tar']
    }

    # Створення порожніх списків для файлів кожної категорії та невідомих розширень
    files_by_type = {category: [] for category in file_types}
    unknown_extensions = []

    # Перебір елементів у вказаному каталозі
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # Перевірка, чи елемент є файлом
        if os.path.isfile(item_path):
            # Визначення розширення файлу
            extension = item.split('.')[-1]
            added_to_category = False

            # Перевірка, до якої категорії належить файл
            for category, extensions in file_types.items():
                if extension in extensions:
                    # Нормалізація імені файлу
                    normalized_name = normalize(item.split('.')[0]) + '.' + extension
                    new_item_path = os.path.join(folder_path, normalized_name)

                    # Перевірка, чи ім'я файлу несуперечить нормалізованому імені і чи файл не існує
                    if item_path != new_item_path:
                        if os.path.exists(new_item_path):
                            added_to_category = True
                            break

                        # Перейменування файлу
                        os.rename(item_path, new_item_path)

                    # Додавання файлу до відповідної категорії
                    files_by_type[category].append(normalized_name)
                    added_to_category = True
                    break

            # Якщо розширення не належить жодній категорії
            if not added_to_category:
                unknown_extensions.append(item)

        # Якщо елемент є папкою, рекурсивний виклик для обробки підпапок
        elif os.path.isdir(item_path):
            subfolder_files, subfolder_unknown = scan_folder(item_path)

            # Додавання файлів та невідомих розширень з підпапки до загального списку
            for category, files in subfolder_files.items():
                files_by_type[category].extend(files)

            unknown_extensions.extend(subfolder_unknown)

            # Нормалізація імені папки
            normalized_name = normalize(item)
            new_item_path = os.path.join(folder_path, normalized_name)

            # Перевірка, чи ім'я папки несуперечить нормалізованому імені і чи папка не існує
            if item_path != new_item_path:
                if os.path.exists(new_item_path):
                    continue

                # Перейменування папки
                os.rename(item_path, new_item_path)

    # Повертаємо результат - файли за категоріями та невідомі розширення
    return files_by_type, unknown_extensions
