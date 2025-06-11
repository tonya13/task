import os
import base64
import argparse

# Функция шифрования с использованием OTP
def encrypt(message, key):
    # Преобразуем сообщение в байты
    message_bytes = message.encode('utf-8')
    
    if len(key) != len(message_bytes):
        raise ValueError("Длина ключа должна совпадать с длиной сообщения.")

    # Применяем XOR между каждым байтом сообщения и ключа
    encrypted_bytes = bytes([m ^ k for m, k in zip(message_bytes, key)])
    return encrypted_bytes

# Функция дешифрования с использованием OTP
def decrypt(ciphertext, key):
    if len(key) != len(ciphertext):
        raise ValueError("Длина ключа должна совпадать с длиной шифротекста.")

    # Применяем XOR между каждым байтом шифротекста и ключа
    decrypted_bytes = bytes([c ^ k for c, k in zip(ciphertext, key)])
    # Декодируем байты в строку
    try:
        return decrypted_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Не удалось декодировать расшифрованный текст. Возможно, ключ или шифротекст повреждены.")

# Функция для сохранения данных в файл
def save_to_file(data, filename):
    try:
        with open(filename, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        return False

# Функция для загрузки данных из файла
def load_from_file(filename):
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

# Основная часть программы
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Шифрование и дешифрование с использованием одноразового блокнота (OTP)')
    parser.add_argument('--mode', choices=['encrypt', 'decrypt'], default='encrypt', help='Режим работы: шифрование или дешифрование')
    parser.add_argument('--key-file', help='Файл для сохранения/загрузки ключа')
    parser.add_argument('--message-file', help='Файл для сохранения/загрузки сообщения')
    parser.add_argument('--ciphertext-file', help='Файл для сохранения/загрузки шифротекста')
    args = parser.parse_args()

    if args.mode == 'encrypt':
        # Запрашиваем у пользователя текст для шифрования
        message = input("Введите текст для шифрования: ")

        # Преобразуем сообщение в байты
        message_bytes = message.encode('utf-8')

        # Генерируем ключ той же длины, что и байтовое представление сообщения
        key = os.urandom(len(message_bytes))
        key_b64 = base64.b64encode(key).decode('utf-8')
        print("\nСгенерированный ключ (в Base64):\n", key_b64)

        # Сохраняем ключ в файл, если указан путь
        if args.key_file:
            if save_to_file(key, args.key_file):
                print(f"Ключ сохранен в файл: {args.key_file}")

        # Шифруем текст
        try:
            encrypted_bytes = encrypt(message, key)
            encrypted_b64 = base64.b64encode(encrypted_bytes).decode('utf-8')
            print("\nЗашифрованный текст (в Base64):\n", encrypted_b64)

            # Сохраняем шифротекст в файл, если указан путь
            if args.ciphertext_file:
                if save_to_file(encrypted_bytes, args.ciphertext_file):
                    print(f"Шифротекст сохранен в файл: {args.ciphertext_file}")
                    
            # Проверочная расшифровка
            decrypted_text = decrypt(encrypted_bytes, key)
            print("\nПроверка расшифровки:\n", decrypted_text)
            
        except ValueError as e:
            print("\nОшибка при шифровании текста:\n", e)

    elif args.mode == 'decrypt':
        # Загружаем ключ
        key = None
        if args.key_file:
            key = load_from_file(args.key_file)
            if key:
                print(f"Ключ загружен из файла: {args.key_file}")
        
        if not key:
            key_b64 = input("Введите ключ в формате Base64: ")
            try:
                key = base64.b64decode(key_b64)
            except:
                print("Ошибка декодирования ключа. Проверьте формат Base64.")
                exit(1)

        # Загружаем шифротекст
        ciphertext = None
        if args.ciphertext_file:
            ciphertext = load_from_file(args.ciphertext_file)
            if ciphertext:
                print(f"Шифротекст загружен из файла: {args.ciphertext_file}")
        
        if not ciphertext:
            ciphertext_b64 = input("Введите шифротекст в формате Base64: ")
            try:
                ciphertext = base64.b64decode(ciphertext_b64)
            except:
                print("Ошибка декодирования шифротекста. Проверьте формат Base64.")
                exit(1)

        # Дешифруем текст
        try:
            decrypted_text = decrypt(ciphertext, key)
            print("\nРасшифрованный текст:\n", decrypted_text)
            
            # Сохраняем расшифрованное сообщение в файл, если указан путь
            if args.message_file:
                if save_to_file(decrypted_text.encode('utf-8'), args.message_file):
                    print(f"Расшифрованный текст сохранен в файл: {args.message_file}")
                    
        except ValueError as e:
            print("\nОшибка при расшифровке текста:\n", e)
