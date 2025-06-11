# Функция шифрования обобщенным шифром Цезаря
def encrypt(key, message):
    return ''.join(chr((ord(c) + key) % 65536) for c in message)

# Функция дешифрования обобщенным шифром Цезаря
def decrypt(key, message):
    return ''.join(chr((ord(c) - key) % 65536) for c in message)

# Функция для оценки вероятности того, что текст является осмысленным
def score_text(text, language='ru'):
    # Наиболее частые буквы в разных языках
    common_chars = {
        'ru': {
            ' ': 0.175, 'о': 0.110, 'е': 0.085, 'а': 0.080, 'и': 0.074, 
            'н': 0.067, 'т': 0.063, 'с': 0.055, 'р': 0.047, 'в': 0.045
        },
        'en': {
            ' ': 0.183, 'e': 0.120, 't': 0.091, 'a': 0.081, 'o': 0.077, 
            'i': 0.073, 'n': 0.070, 's': 0.063, 'r': 0.060, 'h': 0.059
        }
    }
    
    # Используем выбранный язык или русский по умолчанию
    char_freqs = common_chars.get(language.lower(), common_chars['ru'])
    
    # Подсчитываем символы в тексте
    from collections import Counter
    text_length = len(text)
    if text_length == 0:
        return 0
    
    char_counts = Counter(text.lower())
    
    # Рассчитываем оценку текста на основе частотного соответствия
    score = 0
    for char, expected_freq in char_freqs.items():
        actual_freq = char_counts.get(char, 0) / text_length
        # Чем ближе частота к ожидаемой, тем выше оценка
        score += (1 - abs(actual_freq - expected_freq)) * expected_freq
    
    return score

# Функция взлома шифра Цезаря с использованием частотного анализа.
def break_cipher(text, language='ru', max_candidates=3):
    from collections import Counter
    
    if not text:
        return [], None
    
    # Подсчитываем частоту символов
    counter = Counter(text)
    
    # Получаем частые символы в тексте
    most_common_chars = [char for char, _ in counter.most_common(10)]
    
    # Наиболее частые символы в выбранном языке
    common_chars = {
        'ru': [' ', 'о', 'е', 'а', 'и', 'н', 'т', 'с', 'р', 'в'],
        'en': [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h']
    }
    
    # Используем выбранный язык или русский по умолчанию
    freq_chars = common_chars.get(language.lower(), common_chars['ru'])
    
    # Пробуем разные комбинации наиболее частых символов
    candidates = []
    for cipher_char in most_common_chars:
        for plain_char in freq_chars:
            key = (ord(cipher_char) - ord(plain_char)) % 65536
            decrypted = decrypt(key, text)
            score = score_text(decrypted, language)
            candidates.append((decrypted, key, score))
    
    # Сортируем по оценке (от лучшей к худшей)
    candidates.sort(key=lambda x: x[2], reverse=True)
    
    # Возвращаем лучшие варианты
    return candidates[:max_candidates]

# Основная часть программы
if __name__ == "__main__":
    # Получаем ключ от пользователя
    try:
        key = int(input("Введите ключ для шифрования (целое число): "))
    except ValueError:
        print("Ошибка: ключ должен быть целым числом!")
        exit(1)
    
    # Получаем текст для шифрования
    plain_text = input("Введите текст для шифрования: ")
    
    # Шифруем текст
    encrypted_text = encrypt(key, plain_text)
    print("\nЗашифрованный текст:\n", encrypted_text)
    
    # Определяем язык для анализа
    language = input("Выберите язык для анализа (ru/en), по умолчанию русский: ").lower()
    if language not in ['ru', 'en']:
        language = 'ru'
    
    # Взламываем шифр без знания ключа
    print("\nПытаемся восстановить текст...")
    candidates = break_cipher(encrypted_text, language)
    
    if candidates:
        print("\nТоп вариантов расшифровки (в порядке убывания вероятности):")
        for i, (candidate_text, candidate_key, score) in enumerate(candidates, 1):
            print(f"\n{i}. Ключ: {candidate_key}, Оценка: {score:.4f}")
            print(f"Текст: {candidate_text[:100]}{'...' if len(candidate_text) > 100 else ''}")
            
        # Проверяем, был ли ключ определен правильно
        if any(candidate_key == key for _, candidate_key, _ in candidates):
            print("\nУспех! Правильный ключ найден среди кандидатов.")
        else:
            print("\nВнимание: правильный ключ не найден среди кандидатов.")
    else:
        print("\nНе удалось расшифровать текст.")
    
    # Показываем правильную расшифровку для сравнения
    print("\nДля сравнения, правильная расшифровка с исходным ключом:")
    print(decrypt(key, encrypted_text))
