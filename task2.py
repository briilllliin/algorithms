import os
from bitarray._bitarray import bitarray
from bitarray.util import *

def right_shift(array, n):
    res = bitarray(array)
    for _ in range(n):
        res.insert(0, 0)
        res.pop()
    return res

def left_shift(array, n):
    res = bitarray(array)
    for _ in range(n):
        res.pop(0)
        res.append(0)
    return res

def bytestring2bitarray(input_string):
    bits_input_string = bitarray()
    for char in input_string:
        bits_input_string.extend([int(bit) for bit in bin(char)[2:].zfill(8)])
    return bits_input_string

def F(left, key):
    return left_shift(left, 9) ^ (~(right_shift(key, 11) & left))

def get_K_i(K, i):
    return right_shift(K, i * 8)[:32]

def encrypt_block(block, key, n=2):
    size_block = len(block)
    for i in range(n):
        res = bitarray()
        k_i = get_K_i(key, i)
        left = block[:size_block // 2]
        right = block[size_block // 2:]
        temp = F(left, k_i) ^ right
        if i == n - 1:
            new_block = left + temp
        else:
            new_block = temp + left
        res += new_block
        block = res
    return block

def decrypt_block(block, key, n=2):
    size_block = len(block)
    for i in range(n):
        res = bitarray()
        k_i = get_K_i(key, n - i - 1)
        left = block[:size_block // 2]
        right = block[size_block // 2:]
        temp = F(left, k_i) ^ right
        if i == n - 1:
            new_block = left + temp
        else:
            new_block = temp + left
        res += new_block
        block = res
    return block

def encrypt_CBC(plaintext, key, IV, n=2, size_block=64):
    res = bitarray()
    for index_of_block in range(len(plaintext) // size_block):
        block = plaintext[size_block * index_of_block: size_block * (index_of_block + 1)]
        if index_of_block == 0:
            block ^= IV
        else:
            block ^= res[size_block * (index_of_block - 1): size_block * index_of_block]
        encrypted_block = encrypt_block(block, key, n)
        res += encrypted_block
    return res

def decrypt_CBC(plaintext, key, IV, n=2, size_block=64):
    res = bitarray()
    for index_of_block in range(len(plaintext) // size_block):
        block = plaintext[size_block * index_of_block: size_block * (index_of_block + 1)]
        decrypted_block = decrypt_block(block, key, n)
        if index_of_block == 0:
            decrypted_block = decrypted_block ^ IV
        else:
            decrypted_block = decrypted_block ^ plaintext[size_block * (index_of_block - 1): size_block * index_of_block]
        res += decrypted_block
    return res

def encrypt_CFB(plaintext, key, IV, n=2, size_block=64):
    res = bitarray()
    for index_of_block in range(len(plaintext) // size_block):
        block = plaintext[size_block * index_of_block: size_block * (index_of_block + 1)]
        if index_of_block == 0:
            encrypted_block = encrypt_block(IV, key, n)
        else:
            encrypted_block = encrypt_block(res[size_block * (index_of_block - 1): size_block * index_of_block], key, n)
        encrypted_block ^= block
        res += encrypted_block
    return res

def decrypt_CFB(plaintext, key, IV, n=2, size_block=64):
    res = bitarray()
    for index_of_block in range(len(plaintext) // size_block):
        block = plaintext[size_block * index_of_block: size_block * (index_of_block + 1)]
        if index_of_block == 0:
            decrypted_block = encrypt_block(IV, key, n) ^ block
        else:
            decrypted_block = encrypt_block(plaintext[size_block * (index_of_block - 1): size_block * index_of_block], key, n) ^ block
        res += decrypted_block
    return res

input_string = b'Sensitive information is accessible only to authorized users'
input_string = bytes([0] * (8 - len(input_string) % 8)) + input_string
binput_string = bytestring2bitarray(input_string)
key = bytearray(os.urandom(8))
bkey = bytestring2bitarray(key)
n = 10

IV = bytestring2bitarray(bytearray(os.urandom(8)))

print('исходн:', binput_string)
print('_ключ_:', bkey)
print('CBC')
print('зашфрв:', encrypt_CBC(binput_string, bkey, IV, n))
print('расшфр:', decrypt_CBC(encrypt_CBC(binput_string, bkey, IV, n), bkey, IV, n))
print('текст: ', ba2int(decrypt_CBC(encrypt_CBC(binput_string, bkey, IV, n), bkey, IV, n)).to_bytes(21, 'big').decode())
print('CFB')
print('зашфрв:', encrypt_CFB(binput_string, bkey, IV, n))
print('расшфр:', decrypt_CFB(encrypt_CFB(binput_string, bkey, IV, n), bkey, IV, n))
print('текст: ', ba2int(decrypt_CFB(encrypt_CFB(binput_string, bkey, IV, n), bkey, IV, n)).to_bytes(21, 'big').decode())
