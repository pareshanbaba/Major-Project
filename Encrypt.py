def encrypt(W1, W2, W3, W4, K):
    """
    Encryption algorithm for the Sensing Layer.
    
    Args:
        W1, W2, W3, W4 (int): 16-bit unciphered words.
        K (list): 128-bit secret key, represented as a list of 16 subkeys (K1, K2, ..., K16).
    
    Returns:
        C1, C2, C3, C4 (int): 16-bit ciphered words.
    """
    C1, C2, C3, C4 = 0, 0, 0, 0
    
    for i in range(1, 5):
        # (a) SPLIT
        MSB_0 = (W[i-1] & 0xFF00) >> 8
        LSB_0 = W[i-1] & 0x00FF
        
        # (b) XOR1
        MSB_1 = MSB_0 ^ K[4*(i-1)]
        LSB_1 = LSB_0 ^ K[4*(i-1)+1]
        
        # (c) CIRCULAR SHIFT1
        MSB_2 = rotate_byte(MSB_1, K[4*(i-1)+2] & 0x07)
        LSB_2 = rotate_byte(LSB_1, K[4*(i-1)+2] & 0x07)
        
        # (d) XOR2
        MSB_3 = MSB_2 ^ K[4*(i-1)+3]
        LSB_3 = LSB_2 ^ K[4*(i-1)+3]
        
        # (e) CIRCULAR SHIFT2
        MSB_4 = rotate_byte(MSB_3, K[4*(i-1)+1] & 0x07)
        LSB_4 = rotate_byte(LSB_3, K[4*(i-1)+1] & 0x07)
        
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
    
    return C1, C2, C3, C4

def rotate_byte(byte, shift):
    """
    Perform a circular shift on a byte.
    
    Args:
        byte (int): The byte to be shifted.
        shift (int): The number of bits to shift.
    
    Returns:
        int: The shifted byte.
    """
    return ((byte << (shift & 0x07)) | (byte >> (8 - (shift & 0x07)))) & 0xFF
# Example usage
W = [0x1234, 0x5678, 0x9ABC, 0xDEF0]

# 128-bit secret key, represented as a list of 16 subkeys
K = [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0,
     0x21, 0x43, 0x65, 0x87, 0xA9, 0xCB, 0xED, 0xF1]

C1, C2, C3, C4 = encrypt(W[0], W[1], W[2], W[3], K)

print(f"Ciphered words:")
print(f"C1: {C1:04X}")
print(f"C2: {C2:04X}")
print(f"C3: {C3:04X}")
print(f"C4: {C4:04X}")