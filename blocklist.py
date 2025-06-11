from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Шифрование в режиме CBC
def encrypt_cbc(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)  # Генерирует случайный IV автоматически
    iv = cipher.iv
    padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return iv + ciphertext  # Возвращаем IV + зашифрованный текст

# Расшифровка в режиме CBC
def decrypt_cbc(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    encrypted_data = ciphertext[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    padded_plaintext = cipher.decrypt(encrypted_data)
    plaintext = unpad(padded_plaintext, AES.block_size).decode('utf-8')
    return plaintext

# Пример использования
if __name__ == "__main__":
    key = get_random_bytes(16)  # Ключ длиной 128 бит (16 байт)
    text = input("Пример текста для шифрования:")
    print("Оригинал:", text)

    encrypted = encrypt_cbc(text, key)
    print("Зашифровано:", encrypted.hex())

    decrypted = decrypt_cbc(encrypted, key)
    print("Расшифровано:", decrypted)
