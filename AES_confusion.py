from Crypto.Cipher import AES
import random
import os


def confusion_test_aes(num_tests=1000):
    """
    Perform the confusion test on AES.
    num_tests: the number of test cases to run (default: 1000)
    """
    for _ in range(num_tests):
        key = os.urandom_bytes(16)  # 16 bytes (128 bits)
        plaintext1 = os.urandom_bytes(random.randint(16, 32))  # Random plaintext length (between 16 and 32 bytes)
        plaintext2 = os.urandom_bytes(random.randint(16, 32))  # Random plaintext length (between 16 and 32 bytes)

        cipher = AES.new(key, AES.MODE_ECB)
        ciphertext1 = cipher.encrypt(plaintext1)
        ciphertext2 = cipher.encrypt(plaintext2)

        # Calculate the bit difference between the plaintexts and ciphertexts
        plaintext_diff = sum(bin(a ^ b).count('1') for a, b in zip(plaintext1, plaintext2))
        ciphertext_diff = sum(bin(a ^ b).count('1') for a, b in zip(ciphertext1, ciphertext2))

        # Print the differences if they are not close to 50%
        if ciphertext_diff < 0.25 * len(ciphertext1) * 8 or ciphertext_diff > 0.75 * len(ciphertext1) * 8:
            print(f"Plaintext difference: {plaintext_diff} bits")
            print(f"Ciphertext difference: {ciphertext_diff} bits")
            print("Confusion test failed.")
            break
    else:
        print("Confusion test passed.")