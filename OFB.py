#from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from xtea1 import XTEA

# =============================================================================
# plainText = b"Hello World"
# key = b"ANAAREMEREAAAAAA"
# =============================================================================


def ofbEnc(plainText, key, block_size=8):
    pos = 0
    cipherTextChunks = []
    iv = get_random_bytes(block_size)
    originalIV = iv
    cipher = XTEA()
    key=cipher.pack_key(key)
    if len(plainText) % block_size != 0:
        plainText += b"1"
    while len(plainText) % block_size != 0:
        plainText += b"0"
    while pos + block_size <= len(plainText):
        toXor = cipher.xtea_encrypt(key,iv)
        nextPos = pos + block_size
        toEnc = plainText[pos:nextPos]
        cipherText = bytes([toXor[i] ^ toEnc[i] for i in range(block_size)])
        cipherTextChunks.append(cipherText)
        pos += block_size
        iv = toXor
    return (originalIV, cipherTextChunks)


def ofbDec(cipherTextChunks, key, iv, block_size=8):
    plainText = b""
    cipher = XTEA()
    key=cipher.pack_key(key)
    for chunk in cipherTextChunks:
        toXor = cipher.xtea_encrypt(key,iv)
        plainText += bytes([toXor[i] ^ chunk[i] for i in range(block_size)])
        iv = toXor
    while plainText[-1] == 48:
        plainText = plainText[0:-1]
    if plainText[-1] == 49:
        plainText = plainText[0:-1]
    return plainText


# =============================================================================
# iv, result = ofbEnc(plainText, key)
# print("this is the encryption\n")
# print(iv, result)
# 
# plain = ofbDec(result, key, iv)
# print("this is the decryption\n")
# print(plain)
# =============================================================================
