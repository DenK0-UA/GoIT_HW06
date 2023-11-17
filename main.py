def real_len(string):
    # Створення списку недозволених символів
    invalid_chars = ['\n', '\f', '\r', '\t', '\v']

    # Ініціалізація лічильника
    count = 0

    # Перебір кожного символу у рядку
    for char in string:
        # Перевірка, чи символ не належить до недозволених символів
        if char not in invalid_chars:
            # У разі, якщо символ не є недозволеним, збільшуємо лічильник
            count += 1

    # Повернення кількості символів без недозволених символів
    return count


string1 = 'Alex\nKdfe23\t\f\v.\r'
string2 = 'Al\nKdfe23\t\v.\r'

print(real_len(string1))
print(real_len(string2))
