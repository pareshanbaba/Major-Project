import time

def encrypt(W1, W2, W3, W4, K):
    """
    Encryption algorithm for the Sensing Layer.

    Args:
        W1, W2, W3, W4 (int): 16-bit unciphered words.
        K (list): 128-bit secret key, represented as a list of 16 subkeys (K1, K2, ..., K16).

    Returns:
        C1, C2, C3, C4 (int): 16-bit ciphered words.
    """
    start_time = time.perf_counter_ns()

    C1, C2, C3, C4 = 0, 0, 0, 0

    for i in range(1, 5):
        # (a) SPLIT
        MSB_0 = (W[i-1] >> 8) & 0xFF
        LSB_0 = W[i-1] & 0xFF

        # (b) XOR1
        MSB_1 = MSB_0 ^ K[4*(i-1)+1]
        LSB_1 = LSB_0 ^ K[4*(i-1)+2]

        # (c) CIRCULAR SHIFT1
        shift = K[4*(i-1)+3] & 0x07
        MSB_2 = ((MSB_1 << shift) | (MSB_1 >> (8 - shift))) & 0xFF
        LSB_2 = ((LSB_1 << shift) | (LSB_1 >> (8 - shift))) & 0xFF

        # (d) XOR2
        MSB_3 = MSB_2 ^ K[4*(i-1)+1]
        LSB_3 = LSB_2 ^ K[4*(i-1)+1]

        # (e) CIRCULAR SHIFT2
        shift = K[4*(i-1)+2] & 0x07
        MSB_4 = ((MSB_3 << shift) | (MSB_3 >> (8 - shift))) & 0xFF
        LSB_4 = ((LSB_3 << shift) | (LSB_3 >> (8 - shift))) & 0xFF

        # (f) SWAP
        MSB_5 = LSB_4
        LSB_5 = MSB_4

        # Assemble the ciphered word
        if i == 1:
            C1 = (MSB_5 << 8) | LSB_5
        elif i == 2:
            C2 = (MSB_5 << 8) | LSB_5
        elif i == 3:
            C3 = (MSB_5 << 8) | LSB_5
        else:
            C4 = (MSB_5 << 8) | LSB_5

    end_time = time.perf_counter_ns()
    execution_time = (end_time - start_time) / 1000
    print(f"Encryption time: {execution_time:.2f} microseconds")

    return C1, C2, C3, C4

# Example usage
W = [0x1234, 0x5678, 0x9ABC, 0xDEF0]
K = [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0, 0x21, 0x43, 0x65, 0x87, 0xA9, 0xCB, 0xED, 0xF1]

C1, C2, C3, C4 = encrypt(W[0], W[1], W[2], W[3], K)
print(f"Ciphered words:")
print(f"C1: {C1:04X}")
print(f"C2: {C2:04X}")
print(f"C3: {C3:04X}")
print(f"C4: {C4:04X}")