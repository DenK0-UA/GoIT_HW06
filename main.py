import os
import zipfile
import shutil

def organize_files(files, destination_path):
    # Перебираем каждую категорию и список файлов в словаре files
    for category, file_list in files.items():
        # Создаем путь категории внутри пути назначения
        category_path = os.path.join(destination_path, category)
        # Создаем директорию категории, если она не существует
        os.makedirs(category_path, exist_ok=True)

        # Обрабатываем каждый файл в списке файлов
        for file in file_list:
            # Создаем полный путь к файлу внутри пути назначения
            file_path = os.path.join(destination_path, file)

            # Если категория - "archives"
            if category == 'archives':
                # Извлекаем имя архива без расширения
                archive_name = os.path.splitext(file)[0]
                # Создаем путь к архиву внутри категории
                archive_path = os.path.join(category_path, archive_name)
                # Создаем директорию архива, если она не существует
                os.makedirs(archive_path, exist_ok=True)

                # Если файл является zip-архивом
                if zipfile.is_zipfile(file_path):
                    # Распаковываем содержимое архива в путь архива
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(archive_path)
                    # Удаляем исходный zip-файл
                    os.remove(file_path)
                else:
                    # Если формат архива не поддерживается, выводим сообщение
                    print(f"Unsupported archive format: {file}")

            # Если категория не является "archives"
            else:
                # Создаем новый путь файла внутри категории
                new_file_path = os.path.join(category_path, file)
                # Перемещаем файл в новый путь
                shutil.move(file_path, new_file_path)