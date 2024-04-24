import os
from bitarray import bitarray


def right_shift(array, n):
    res = array.copy()
    for _ in range(n):
        res.insert(0, False)
        del res[-1]
    return res


def left_shift(array, n):
    res = array.copy()
    for _ in range(n):
        res.append(False)
        del res[0]
    return res


def bytestring2bitarray(input_string):
    bits_input_string = bitarray()
    for char in input_string:
        bits_input_string.extend(format(char, '08b'))
    return bits_input_string


def F(left, key):
    return left_shift(left, 9) ^ (~(right_shift(key, 11) & left))


def get_K_i(K, i):
    return right_shift(K, i * 8)[:32]


def encrypt(plaintext, key, n=2, size_block=64):
    for i in range(n):
        res = bitarray()
        k_i = get_K_i(key, i)
        for index_of_block in range(len(plaintext) // size_block):
            block = plaintext[size_block * index_of_block: size_block * (index_of_block + 1)]
            left = block[:size_block // 2]
            right = block[size_block // 2:]
            temp = F(left, k_i) ^ right
            new_block = (left + temp) if i == n - 1 else (temp + left)
            res.extend(new_block)
        plaintext = res
    return plaintext


def decrypt(plaintext, key, n=2, size_block=64):
    for i in range(n):
        res = bitarray()
        k_i = get_K_i(key, n - i - 1)
        for index_of_block in range(len(plaintext) // size_block):
            block = plaintext[size_block * index_of_block: size_block * (index_of_block + 1)]
            left = block[:size_block // 2]
            right = block[size_block // 2:]
            temp = F(left, k_i) ^ right
            new_block = (left + temp) if i == n - 1 else (temp + left)
            res.extend(new_block)
        plaintext = res
    return plaintext


input_string = b'Sensitive information is accessible only to authorized users'
input_string = bytes([0] * (8 - len(input_string) % 8)) + input_string
binput_string = bytestring2bitarray(input_string)
key = bytearray(os.urandom(8))
bkey = bytestring2bitarray(key)
n = 10

print('исходн:', binput_string)
print('_ключ_:', bkey)
encrypted = encrypt(binput_string, bkey, n)
print('зашфрв:', encrypted)
decrypted = decrypt(encrypted, bkey, n)
print('расшфр:', decrypted)
print('текст: ', decrypted.tobytes().decode())
