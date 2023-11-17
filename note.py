# Імпорт функції scan_folder зі сканованого файлу
from scan_folder import scan_folder

# Шлях до тестової папки
test_folder_path = 'C:/Users/denid/Desktop/test_garbage_folder_etalon'

# Виклик функції scan_folder
files_by_type, unknown_extensions = scan_folder(test_folder_path)

# Виведення результатів
print("Файли за категоріями:")
for category, files in files_by_type.items():
    print(f"{category}: {files}")

print("Невідомі розширення:")
print(unknown_extensions)