import os  # Імпортуємо модуль os для взаємодії з операційною системою
import shutil  # Імпортуємо модуль shutil для виконання операцій з файлами та папками

def move_files(source, destination):
    # Функція, що переміщує файли з одного місця в інше
    # Приймає два аргументи: source - початковий шлях, destination - шлях призначення

    for root, dirs, files in os.walk(source):
        # Цикл, що проходить через всі папки та файли у вказаній початковій папці та її підпапках
        # Використовується функція os.walk() для отримання списку папок та файлів

        for file in files:
            # Цикл, що проходить через кожен файл у списку файлів

            file_path = os.path.join(root, file)
            # Об'єднуємо шлях батьківської папки (root) з назвою файлу (file)
            # за допомогою функції os.path.join()
            # Отримуємо повний шлях до файлу

            destination_path = os.path.join(destination, file)
            # Об'єднуємо шлях призначення (destination) з назвою файлу (file)
            # за допомогою функції os.path.join()
            # Отримуємо повний шлях до місця призначення файлу

            shutil.move(file_path, destination_path)
            # Переміщуємо файл з початкового шляху (file_path) до шляху призначення (destination_path)
