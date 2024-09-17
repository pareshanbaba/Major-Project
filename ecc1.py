from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Generate keys
private_key = ec.generate_private_key(ec.SECP256K1())  # Receiver Alice's private key
public_key = private_key.public_key() 

# Encryption
sender_private_key = ec.generate_private_key(ec.SECP256K1())  # Bob's ephemeral key
sender_public_key = sender_private_key.public_key()

shared_key = sender_private_key.exchange(ec.ECDH(), public_key) 
derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'encryption key'  # Adjust 'info' as needed
).derive(shared_key)

cipher = Cipher(algorithms.AES(derived_key), modes.GCM(derived_key[:12]))
encryptor = cipher.encryptor()

plaintext = b"My secret message"
ciphertext = encryptor.update(plaintext) + encryptor.finalize()
tag = encryptor.tag
print(tag)
# ... Send sender_public_key, ciphertext, and tag to the receiver

# Decryption
derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'encryption key'
).derive(private_key.exchange(ec.ECDH(), sender_public_key)) 

cipher = Cipher(algorithms.AES(derived_key), modes.GCM(derived_key[:12], tag))
decryptor = cipher.decryptor()
decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

print(decrypted_data.decode()) 
