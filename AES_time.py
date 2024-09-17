from Crypto.Cipher import AES
import time
from Crypto.Util.Padding import pad, unpad

def aes_encrypt(W1, W2, W3, W4, key):
    """
    AES encryption for the Sensing Layer.
    
    Args:
        W1, W2, W3, W4 (int): 16-bit unciphered words.
        key (bytes): 128-bit secret key.
    
    Returns:
        C1, C2, C3, C4 (int): 16-bit ciphered words.
    """
    start_time = time.perf_counter_ns()
    
    # Combine the 16-bit words into a 64-bit plaintext
    plaintext = (W1 << 48) | (W2 << 32) | (W3 << 16) | W4
    
    # Pad the plaintext to the block size
    plaintext_bytes = plaintext.to_bytes(8, byteorder='big')
    padded_plaintext = pad(plaintext_bytes, AES.block_size)
    
    # Encrypt the plaintext using AES
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(padded_plaintext)
    
    # Extract the 16-bit ciphered words
    C1 = int.from_bytes(ciphertext[0:2], byteorder='big')
    C2 = int.from_bytes(ciphertext[2:4], byteorder='big')
    C3 = int.from_bytes(ciphertext[4:6], byteorder='big')
    C4 = int.from_bytes(ciphertext[6:8], byteorder='big')
    
    end_time = time.perf_counter_ns()
    execution_time = (end_time - start_time) / 1000  # Convert to microseconds
    print(f"AES Encryption time: {execution_time:.9f} microseconds")
    
    return C1, C2, C3, C4

# Example usage
W = [0x1234, 0x5678, 0x9ABC, 0xDEF0]

# 128-bit secret key
key = b'\x12\x34\x56\x78\x9A\xBC\xDE\xF0\x21\x43\x65\x87\xA9\xCB\xED\xF1'

C1, C2, C3, C4 = aes_encrypt(W[0], W[1], W[2], W[3], key)

print(f"Ciphered words:")
print(f"C1: {C1:04X}")
print(f"C2: {C2:04X}")
print(f"C3: {C3:04X}")
print(f"C4: {C4:04X}")