# Функция для размножения ключа до длины сообщения
def extend_key(key, length):
    if not key:
        raise ValueError("Ключ не может быть пустым")
    return (key * (length // len(key) + 1))[:length]

# Функция шифрования шифром Виженера
def encrypt(key, message, alphabet_mode=False):
    """
    Шифрует сообщение с помощью шифра Виженера.
    
    Args:
        key: Ключ шифрования
        message: Сообщение для шифрования
        alphabet_mode: Если True, использует алфавитный режим для латиницы/кириллицы,
                       иначе использует обобщенный Юникод-режим
    """
    if not message:
        return ""
        
    # Размножаем ключ до длины сообщения
    extended_key = extend_key(key, len(message))
    encrypted_chars = []
    
    if not alphabet_mode:
        # Обобщенный режим для всех символов Юникода
        for m_char, k_char in zip(message, extended_key):
            encrypted_char = chr((ord(m_char) + ord(k_char)) % 65536)
            encrypted_chars.append(encrypted_char)
    else:
        # Алфавитный режим для латиницы и кириллицы
        key_idx = 0
        for char in message:
            if 'A' <= char <= 'Z':
                # Для английских заглавных букв
                shift = ord(extended_key[key_idx].upper()) % 26
                if 'A' <= extended_key[key_idx].upper() <= 'Z':
                    shift = ord(extended_key[key_idx].upper()) - ord('A')
                encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                key_idx += 1
            elif 'a' <= char <= 'z':
                # Для английских строчных букв
                shift = ord(extended_key[key_idx].upper()) % 26
                if 'A' <= extended_key[key_idx].upper() <= 'Z':
                    shift = ord(extended_key[key_idx].upper()) - ord('A')
                encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                key_idx += 1
            elif 'А' <= char <= 'Я' or char == 'Ё':
                # Для русских заглавных букв
                char_code = ord(char) - ord('А') if char != 'Ё' else 6
                key_char = extended_key[key_idx].upper()
                key_code = ord(key_char) - ord('А') if key_char != 'Ё' and 'А' <= key_char <= 'Я' else 0
                new_code = (char_code + key_code) % 33
                if new_code == 6:
                    encrypted_char = 'Ё'
                else:
                    if new_code > 6:
                        new_code -= 1
                    encrypted_char = chr(new_code + ord('А'))
                key_idx += 1
            elif 'а' <= char <= 'я' or char == 'ё':
                # Для русских строчных букв
                char_code = ord(char) - ord('а') if char != 'ё' else 6
                key_char = extended_key[key_idx].lower()
                key_code = ord(key_char) - ord('а') if key_char != 'ё' and 'а' <= key_char <= 'я' else 0
                new_code = (char_code + key_code) % 33
                if new_code == 6:
                    encrypted_char = 'ё'
                else:
                    if new_code > 6:
                        new_code -= 1
                    encrypted_char = chr(new_code + ord('а'))
                key_idx += 1
            else:
                # Другие символы оставляем без изменений
                encrypted_char = char
            
            encrypted_chars.append(encrypted_char)
    
    return ''.join(encrypted_chars)

# Функция дешифрования шифра Виженера
def decrypt(key, ciphertext, alphabet_mode=False):
    """
    Дешифрует сообщение, зашифрованное шифром Виженера.
    
    Args:
        key: Ключ шифрования
        ciphertext: Зашифрованное сообщение
        alphabet_mode: Если True, использует алфавитный режим для латиницы/кириллицы,
                       иначе использует обобщенный Юникод-режим
    """
    if not ciphertext:
        return ""
        
    # Размножаем ключ до длины шифротекста
    extended_key = extend_key(key, len(ciphertext))
    decrypted_chars = []
    
    if not alphabet_mode:
        # Обобщенный режим для всех символов Юникода
        for c_char, k_char in zip(ciphertext, extended_key):
            decrypted_char = chr((ord(c_char) - ord(k_char)) % 65536)
            decrypted_chars.append(decrypted_char)
    else:
        # Алфавитный режим для латиницы и кириллицы
        key_idx = 0
        for char in ciphertext:
            if 'A' <= char <= 'Z':
                # Для английских заглавных букв
                shift = ord(extended_key[key_idx].upper()) % 26
                if 'A' <= extended_key[key_idx].upper() <= 'Z':
                    shift = ord(extended_key[key_idx].upper()) - ord('A')
                decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                key_idx += 1
            elif 'a' <= char <= 'z':
                # Для английских строчных букв
                shift = ord(extended_key[key_idx].upper()) % 26
                if 'A' <= extended_key[key_idx].upper() <= 'Z':
                    shift = ord(extended_key[key_idx].upper()) - ord('A')
                decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                key_idx += 1
            elif 'А' <= char <= 'Я' or char == 'Ё':
                # Для русских заглавных букв
                char_code = ord(char) - ord('А') if char != 'Ё' else 6
                key_char = extended_key[key_idx].upper()
                key_code = ord(key_char) - ord('А') if key_char != 'Ё' and 'А' <= key_char <= 'Я' else 0
                new_code = (char_code - key_code) % 33
                if new_code == 6:
                    decrypted_char = 'Ё'
                else:
                    if new_code > 6:
                        new_code -= 1
                    decrypted_char = chr(new_code + ord('А'))
                key_idx += 1
            elif 'а' <= char <= 'я' or char == 'ё':
                # Для русских строчных букв
                char_code = ord(char) - ord('а') if char != 'ё' else 6
                key_char = extended_key[key_idx].lower()
                key_code = ord(key_char) - ord('а') if key_char != 'ё' and 'а' <= key_char <= 'я' else 0
                new_code = (char_code - key_code) % 33
                if new_code == 6:
                    decrypted_char = 'ё'
                else:
                    if new_code > 6:
                        new_code -= 1
                    decrypted_char = chr(new_code + ord('а'))
                key_idx += 1
            else:
                # Другие символы оставляем без изменений
                decrypted_char = char
            
            decrypted_chars.append(decrypted_char)
    
    return ''.join(decrypted_chars)

# Основная часть программы
if __name__ == "__main__":
    try:
        # Запрашиваем у пользователя ключ и текст для шифрования
        key = input("Введите ключ для шифрования (строка): ")
        if not key:
            print("Ошибка: ключ не может быть пустым")
            exit(1)
            
        message = input("Введите текст для шифрования: ")
        
        # Выбор режима шифрования
        mode_choice = input("Использовать алфавитный режим? (да/нет, по умолчанию - нет): ").lower()
        alphabet_mode = mode_choice in ('да', 'yes', 'y', 'д')
        
        # Шифруем текст
        encrypted_text = encrypt(key, message, alphabet_mode)
        print("\nЗашифрованный текст:\n", encrypted_text)
        
        # Дешифруем текст
        decrypted_text = decrypt(key, encrypted_text, alphabet_mode)
        print("\nРасшифрованный текст:\n", decrypted_text)
        
        # Проверка корректности
        if decrypted_text == message:
            print("\nПроверка пройдена: расшифрованный текст совпадает с исходным!")
        else:
            print("\nОшибка: расшифрованный текст не совпадает с исходным.")
            
    except Exception as e:
        print(f"Произошла ошибка: {e}")
