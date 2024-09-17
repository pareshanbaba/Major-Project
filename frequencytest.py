import time
from collections import Counter

def rot_msb(word, shift):
    """Rotate the most significant byte of a 16-bit word by the given shift"""
    msb = (word >> 8) & 0xFF
    shift = shift % 8  # Ensure shift value is between 0 and 7
    msb = ((msb << shift) | (msb >> (8 - shift))) & 0xFF
    return (word & 0x00FF) | (msb << 8)

def rot_lsb(word, shift):
    """Rotate the least significant byte of a 16-bit word by the given shift"""
    lsb = word & 0xFF
    shift = shift % 8  # Ensure shift value is between 0 and 7
    lsb = ((lsb << shift) | (lsb >> (8 - shift))) & 0xFF
    return (word & 0xFF00) | lsb

def encrypt(words, key):
    """Encrypt four 16-bit words using the given 128-bit key"""
    ciphered_words = []
    for i in range(4):
        msb0 = (words[i] >> 8) & 0xFF
        lsb0 = words[i] & 0xFF

        msb1 = msb0 ^ key[4 * (i - 1) + 1]
        lsb1 = lsb0 ^ key[4 * (i - 1) + 1]

        msb2 = rot_msb(msb1, key[4 * (i - 1) + 2])
        lsb2 = rot_lsb(lsb1, key[4 * (i - 1) + 2])

        msb3 = msb2 ^ key[4 * (i - 1) + 3]
        lsb3 = lsb2 ^ key[4 * (i - 1) + 3]

        msb4 = rot_msb(msb3, key[4 * (i - 1) + 4])
        lsb4 = rot_lsb(lsb3, key[4 * (i - 1) + 4])

        msb5 = lsb4
        lsb5 = msb4

        ciphered_words.append((msb5 << 8) | lsb5)

    return ciphered_words

# Example usage for encryption
unciphered_words = [0x1234, 0x5678, 0x9ABC, 0xDEF0]
key = [0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF]

ciphered_words = encrypt(unciphered_words, key)
print("Ciphered words:", ciphered_words)

# Frequency analysis
ciphered_text_dataset = []
for plaintext, key in [(b'Hello, World!', [0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF]),
                       (b'This is a test.', [0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10, 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF]),
                       # Add more plaintext and key combinations here
                      ]:
    ciphered_text = encrypt([int.from_bytes(plaintext[i:i+2], 'big') for i in range(0, len(plaintext), 2)], key)
    ciphered_text_dataset.extend([(byte_value >> 8, byte_value & 0xFF) for byte_value in ciphered_text])

byte_values = [byte for byte_pair in ciphered_text_dataset for byte in byte_pair]
byte_frequencies = Counter(byte_values)

print("\nByte Frequencies:")
for byte_value, frequency in byte_frequencies.items():
    print(f"Byte value: {byte_value}, Frequency: {frequency}")