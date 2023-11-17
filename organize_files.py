import os
import shutil
import zipfile

def organize_files(files, destination_path):
    # Перебираємо словник файлів та їх категорій
    for category, file_list in files.items():
        # Формуємо шлях до категорії у визначеному каталозі призначення
        category_path = os.path.join(destination_path, category)
        # Створюємо каталог, якщо його ще не існує
        os.makedirs(category_path, exist_ok=True)

        # Перебираємо файли у поточній категорії
        for file in file_list:
            # Формуємо повний шлях до поточного файлу
            file_path = os.path.join(destination_path, file)

            # Перевіряємо, чи категорія є "archives"
            if category == 'archives':
                # Витягуємо ім'я архіву без розширення
                archive_name = os.path.splitext(file)[0]
                # Формуємо шлях до каталогу архіву у визначеній категорії
                archive_path = os.path.join(category_path, archive_name)
                # Створюємо каталог архіву, якщо його ще не існує
                os.makedirs(archive_path, exist_ok=True)

                # Перевіряємо, чи файл є архівом формату zip
                if zipfile.is_zipfile(file_path):
                    # Витягуємо вміст архіву у каталог архіву
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(archive_path)
                    # Видаляємо оригінальний архів
                    os.remove(file_path)
                else:
                    # Виводимо повідомлення про непідтримуваний формат архіву
                    print(f"Unsupported archive format: {file}")

            # Якщо категорія не є "archives"
            else:
                # Формуємо новий шлях для файлу у визначеній категорії
                new_file_path = os.path.join(category_path, file)
                # Переміщуємо файл у новий каталог
                shutil.move(file_path, new_file_path)
