def encrypt(k, m):
    return ''.join(map(chr, [(ord(c) + k) % 65536 for c in m]))

def decrypt(k, m):
    return ''.join(map(chr, [(ord(c) - k) % 65536 for c in m]))

# Запрос ключа и текста от пользователя
key = int(input("Введите ключ для шифрования (целое число): "))
text = input("Введите текст для шифрования: ")

# Шифрование текста
encrypted_text = encrypt(key, text)
print("Зашифрованный текст:", encrypted_text)

# Дешифрование текста
decrypted_text = decrypt(key, encrypted_text)
print("Расшифрованный текст:", decrypted_text)
