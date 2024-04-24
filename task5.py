import matplotlib.pyplot as plt


def get_sorted_array(d):
    sorted_list = list(d.items())
    sorted_list.sort(key=lambda i: i[1])
    return [i[0] for i in sorted_list]


def count_ngrams(text, n):
    res = {}
    for i in range(len(text) - n + 1):
        if all(text[i + j].isalpha() for j in range(n)):
            ngram = text[i:i + n]
            if ngram in res:
                res[ngram] += 1
            else:
                res[ngram] = 1

    res = list(reversed(get_sorted_array(res)))
    return res[:11] if n == 2 else res[:6]


def decrypt(text, letter_freq):
    current_chars = {}
    res = ''

    count = sum(1 for char in text if char.isalpha() and char == char.lower())
    for char in text:
        if char.isalpha() and char == char.lower():
            if char in current_chars:
                current_chars[char] += 1
            else:
                current_chars[char] = 1

    print(current_chars)
    for char in current_chars:
        current_chars[char] = current_chars[char] * 100 / count

    sorted_freq = list(reversed(get_sorted_array(letter_freq)))
    sorted_current = list(reversed(get_sorted_array(current_chars)))

    correspondence = {}
    for i in range(len(sorted_current)):
        correspondence[sorted_current[i]] = sorted_freq[i]

    correspondence['ю'] = 'т'
    correspondence['ц'] = 'о'
    correspondence['и'] = 'к'
    correspondence['ф'] = 'г'
    correspondence['я'] = 'д'
    correspondence['м'] = 'а'
    correspondence['б'] = 'ы'
    correspondence['щ'] = 'в'
    correspondence['а'] = 'ч'
    correspondence['ъ'] = 'н'
    correspondence['д'] = 'е'
    correspondence['с'] = 'р'
    correspondence['ж'] = 'м'
    correspondence['в'] = 'щ'
    correspondence['й'] = 'с'
    correspondence['э'] = 'и'
    correspondence['е'] = 'з'
    correspondence['л'] = 'ж'
    correspondence['н'] = 'я'
    correspondence['т'] = 'ю'
    correspondence['ь'] = 'л'
    correspondence['з'] = 'п'
    correspondence['о'] = 'х'
    correspondence['к'] = 'й'
    correspondence['п'] = 'б'
    correspondence['ы'] = 'у'
    correspondence['у'] = 'ш'
    correspondence['ч'] = 'ь'
    correspondence['ш'] = 'ц'

    for char in text:
        if char.isalpha():
            if char in correspondence:
                res += correspondence[char]
            else:
                res += char
        else:
            res += char
    return res, correspondence, current_chars


def show_result(text, letter_freq, zam, correspondence):
    print('Расшифрованный текст: ')
    print(text)

    plt.bar(letter_freq.keys(), letter_freq.values(), width=0.5, color='g')
    plt.show()

    sorted_zam = list(zam.items())
    sorted_zam.sort(key=lambda i: i[1])
    sorted_zam = list(reversed(sorted_zam))

    plt.bar([i[0] for i in sorted_zam], [i[1] for i in sorted_zam], width=0.5, color='g')
    plt.show()

    for i in correspondence:
        print(i + ': ' + correspondence[i])


plt.close()

with open('rus_text.txt', encoding='utf8') as file:
    C1 = file.read()

with open('eng_text.txt') as file:
    C2 = file.read().lower()

english_letter_freq = {
    'E': 12.70,
    'T': 9.06,
    'A': 8.17,
    'O': 7.51,
    'I': 6.97,
    'N': 6.75,
    'S': 6.33,
    'H': 6.09,
    'R': 5.99,
    'D': 4.25,
    'L': 4.03,
    'C': 2.78,
    'U': 2.76,
    'M': 2.41,
    'W': 2.36,
    'F': 2.23,
    'G': 2.02,
    'Y': 1.97,
    'P': 1.93,
    'B': 1.29,
    'V': 0.98,
    'K': 0.77,
    'J': 0.15,
    'X': 0.15,
    'Q': 0.10,
    'Z': 0.07
}

russian_letter_freq = {
    'О': 11.18,
    'Е': 8.95,
    'А': 7.64,
    'И': 7.09,
    'Н': 6.78,
    'Т': 6.09,
    'С': 4.97,
    'Л': 4.96,
    'В': 4.38,
    'Р': 4.23,
    'К': 3.30,
    'М': 3.17,
    'Д': 3.09,
    'П': 2.47,
    'Ы': 2.36,
    'У': 2.22,
    'Б': 2.01,
    'Я': 1.96,
    'Ь': 1.84,
    'Г': 1.72,
    'З': 1.48,
    'Ч': 1.40,
    'Й': 1.21,
    'Ж': 1.01,
    'Х': 0.95,
    'Ш': 0.72,
    'Ю': 0.47,
    'Ц': 0.39,
    'Э': 0.36,
    'Щ': 0.30,
    'Ф': 0.21,
    'Ъ': 0.02
}

print(count_ngrams(C1, 2))
print(count_ngrams(C1, 3))
res_rus, rus_sootv, chast = decrypt(C1, russian_letter_freq)
show_result(res_rus, russian_letter_freq, chast, rus_sootv)
