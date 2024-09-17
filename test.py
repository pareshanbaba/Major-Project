import time

def encrypt(W1, W2, W3, W4, K):
    start_time = time.perf_counter_ns()
    C1, C2, C3, C4 = [], [], [], []
    plaintext_words = [W1, W2, W3, W4]

    for i, W in enumerate(plaintext_words, start=1):
        # (a) SPLIT
        MSB_0 = (W >> 8) & 0xFF
        LSB_0 = W & 0xFF

        # (b) XOR1
        MSB_1 = MSB_0 ^ K[4*(i-1)+0]
        LSB_1 = LSB_0 ^ K[4*(i-1)+1]

        # (c) CIRCULAR SHIFT
        shift_amount = K[4*(i-1)+2] & 0x07  # Mask the shift amount to 0-7 bits
        MSB_2 = ((MSB_1 << shift_amount) | (MSB_1 >> (8 - shift_amount))) & 0xFF
        LSB_2 = ((LSB_1 << shift_amount) | (LSB_1 >> (8 - shift_amount))) & 0xFF

        # (d) SCRAMBLING
        MSB_3 = SBOX[MSB_2 % len(SBOX)]
        LSB_3 = SBOX[LSB_2 % len(SBOX)]

        # (e) XOR2
        MSB_4 = MSB_3 ^ K[4*(i-1)+3]
        LSB_4 = LSB_3 ^ K[4*(i-1)+3]

        # (f) SWAP
        MSB_5 = LSB_4
        LSB_5 = MSB_4

        if i == 1:
            C1 = [MSB_5, LSB_5]
        elif i == 2:
            C2 = [MSB_5, LSB_5]
        elif i == 3:
            C3 = [MSB_5, LSB_5]
        else:
            C4 = [MSB_5, LSB_5]

    end_time = time.perf_counter_ns()
    encryption_time = (end_time - start_time) / 1000  # Time in microseconds
    return C1, C2, C3, C4, encryption_time

# Define the 128-bit secret key (16 subkeys of 8 bits each)
K = [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0, 0x21, 0x43, 0x65, 0x87, 0xA9, 0xCB, 0xED, 0x0F]

# Define the S-box (substitute box) for scrambling
SBOX = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76]

# Example usage
W1 = 0x1253
W2 = 0x5676
W3 = 0x9ABC
W4 = 0xDEF0

C1, C2, C3, C4, encryption_time = encrypt(W1, W2, W3, W4, K)
print("Ciphered words:")
print("C1 =", C1)
print("C2 =", C2)
print("C3 =", C3)
print("C4 =", C4)
print(f"Encryption time: {encryption_time:.9f} microseconds")


import random
from collections import Counter

def confusion_test(encrypt_func, plaintext_words, key):
    # Encrypt the plaintext words
    C1, C2, C3, C4, _ = encrypt_func(*plaintext_words, key)
    
    # Concatenate the ciphertext bytes
    ciphertext = bytes([byte for word in [C1, C2, C3, C4] for byte in word])
    
    # Calculate the frequency distribution of bytes
    freq_dist = Counter(ciphertext)
    
    # Evaluate the frequency distribution against a uniform distribution
    # (ideally, all bytes should have equal frequency)
    expected_freq = len(ciphertext) / 256
    chi_squared = sum(((freq - expected_freq) ** 2) / expected_freq for freq in freq_dist.values())
    
    # High chi-squared value indicates poor confusion property
    print(f"Confusion test (chi-squared): {chi_squared:.3f}")

def diffusion_test(encrypt_func, plaintext_words, key):
    # Encrypt the original plaintext
    C1, C2, C3, C4, _ = encrypt_func(*plaintext_words, key)
    original_ciphertext = bytes([byte for word in [C1, C2, C3, C4] for byte in word])
    
    # Encrypt the plaintext with a single-bit change
    plaintext_words_flipped = list(plaintext_words)
    plaintext_words_flipped[0] ^= 1  # Flip the first bit of the first word
    C1_flipped, C2_flipped, C3_flipped, C4_flipped, _ = encrypt_func(*plaintext_words_flipped, key)
    flipped_ciphertext = bytes([byte for word in [C1_flipped, C2_flipped, C3_flipped, C4_flipped] for byte in word])
    
    # Calculate the number of bit differences between the ciphertexts
    bit_differences = sum(bin(byte1 ^ byte2).count('1') for byte1, byte2 in zip(original_ciphertext, flipped_ciphertext))
    
    # Evaluate the diffusion property based on the number of bit differences
    # (ideally, a single-bit change in the plaintext should result in approximately 50% bit differences)
    expected_differences = len(original_ciphertext) * 4  # 4 bits per byte
    diffusion_score = abs(bit_differences - expected_differences) / expected_differences
    
    # Low diffusion_score indicates good diffusion property
    print(f"Diffusion test (score): {diffusion_score:.3f}")

# Example usage
def encrypt(W1, W2, W3, W4, K):
    # ... (the original encryption function)
    return C1, C2, C3, C4, encryption_time

# Define the secret key
K = [0x12, 0x34, 0x58, 0x78, 0x9A, 0xBC, 0xDE, 0xF0, 0x21, 0x43, 0x65, 0x87, 0xA9, 0xCB, 0xED, 0x0F]

# Generate random plaintext words
plaintext_words = [random.randint(0, 0xFFFF) for _ in range(4)]

# Perform the confusion and diffusion tests
confusion_test(encrypt, plaintext_words, K)
diffusion_test(encrypt, plaintext_words, K)