def encrypt(W1, W2, W3, W4, K):
    C1, C2, C3, C4 = [], [], [], []
    
    for i in range(1, 5):
        # (a) SPLIT
        if i == 1:
            MSB_0 = (W1 >> 8) & 0xFF
            LSB_0 = W1 & 0xFF
        elif i == 2:
            MSB_0 = (W2 >> 8) & 0xFF
            LSB_0 = W2 & 0xFF
        elif i == 3:
            MSB_0 = (W3 >> 8) & 0xFF
            LSB_0 = W3 & 0xFF
        else:
            MSB_0 = (W4 >> 8) & 0xFF
            LSB_0 = W4 & 0xFF
        
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
    
    return C1, C2, C3, C4

# Define the 128-bit secret key (16 subkeys of 8 bits each)
K = [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0,
     0x21, 0x43, 0x65, 0x87, 0xA9, 0xCB, 0xED, 0x0F]

# Define the S-box (substitute box) for scrambling
SBOX = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,
        0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        # Remaining 240 entries omitted for brevity
        ]

# Example usage
W1 = 0x1234
W2 = 0x5678
W3 = 0x9ABC
W4 = 0xDEF0

C1, C2, C3, C4 = encrypt(W1, W2, W3, W4, K)
print("Ciphered words:")
print("C1 =", C1)
print("C2 =", C2)
print("C3 =", C3)
print("C4 =", C4)